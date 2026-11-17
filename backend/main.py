"""Point d'entrée : serveur HTTP local (http.server) et routes de l'API."""

import json
import os
import re
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import scanner
import storage
import versions

# Dossiers du projet (calculés à partir de l'emplacement de ce fichier,
# comme ça le programme marche peu importe d'où on le lance)
ROOT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT_DIR / "frontend"
CONFIG_PATH = ROOT_DIR / "config.json"

# Valeurs utilisées si une clé manque dans config.json
DEFAULT_CONFIG = {
    "watched_folders": [],
    "history_dir": "history",
    "check_interval": 10,        # secondes entre deux vérifications
    "stabilization_delay": 60,   # secondes sans modification avant une sauvegarde auto
    "host": "127.0.0.1",
    "port": 8000,
}

# État partagé entre le serveur et la surveillance automatique
CONFIG = {}
HISTORY = []   # liste des versions, remplie par versions.create_version()


def load_config():
    """Lit config.json et complète avec les valeurs par défaut."""
    config = dict(DEFAULT_CONFIG)
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            config.update(json.load(f))
    except FileNotFoundError:
        print(f"[config] {CONFIG_PATH} introuvable, valeurs par défaut utilisées")
    except json.JSONDecodeError as e:
        print(f"[config] config.json invalide ({e}), valeurs par défaut utilisées")
    return config


def save_config():
    """Réécrit config.json avec la config actuelle."""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(CONFIG, f, indent=4, ensure_ascii=False)
        f.write("\n")


# ---------------------------------------------------------------------------
# Fonctions de l'API : chacune renvoie (données, code HTTP)
# ---------------------------------------------------------------------------

class ApiError(Exception):
    """Erreur renvoyée au front sous la forme {"error": message}."""

    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message


def main_folder():
    if not CONFIG["watched_folders"]:
        raise ApiError(400, "Aucun dossier surveillé dans config.json")
    return CONFIG["watched_folders"][0]


def get_version(number):
    for version in HISTORY:
        if version["number"] == number:
            return version
    raise ApiError(404, f"Version {number} introuvable")


def api_get_config(body):
    return CONFIG, 200


def api_set_config(body):
    """Modifie check_interval et/ou stabilization_delay depuis le front."""
    for key in ("check_interval", "stabilization_delay"):
        if key in body:
            value = body[key]
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                raise ApiError(400, f"{key} doit être un entier >= 1")
            CONFIG[key] = value
    save_config()
    return CONFIG, 200


def api_folders(body):
    folders = [{"path": f, "exists": Path(f).is_dir()} for f in CONFIG["watched_folders"]]
    return folders, 200


def api_status(body):
    """Changements pas encore sauvegardés depuis la dernière version."""
    last_state = HISTORY[-1]["files"] if HISTORY else {}
    return versions.compare(last_state, scanner.scan(main_folder())), 200


def api_list_versions(body):
    return versions.list_versions(HISTORY), 200


def api_save(body):
    """Sauvegarde manuelle."""
    main_folder()  # vérifie qu'il y a bien un dossier surveillé
    version = versions.save_now(HISTORY, CONFIG, scanner.scan)
    if version is None:
        return {"version": None, "message": "Aucun changement à sauvegarder"}, 200
    return {"version": versions.list_versions([version])[0]}, 201


def api_version_files(body, number):
    version = get_version(int(number))
    files = [{"path": path, "hash": h} for path, h in sorted(version["files"].items())]
    return files, 200


def api_file_content(body, number):
    raise ApiError(501, "Lecture d'un fichier pas encore disponible (storage.py)")


def api_restore(body, number):
    raise ApiError(501, "Restauration pas encore disponible (storage.py / versions.py)")


# (méthode, motif de l'URL, fonction). Les (\d+) sont passés en paramètres.
ROUTES = [
    ("GET",  r"/api/config",                    api_get_config),
    ("POST", r"/api/config",                    api_set_config),
    ("GET",  r"/api/folders",                   api_folders),
    ("GET",  r"/api/status",                    api_status),
    ("GET",  r"/api/versions",                  api_list_versions),
    ("POST", r"/api/versions",                  api_save),
    ("GET",  r"/api/versions/(\d+)/files",      api_version_files),
    ("GET",  r"/api/versions/(\d+)/file",       api_file_content),
    ("POST", r"/api/versions/(\d+)/restore",    api_restore),
]


# ---------------------------------------------------------------------------
# Serveur HTTP
# ---------------------------------------------------------------------------

class Handler(SimpleHTTPRequestHandler):
    """Sert les fichiers du dossier frontend/ et les routes /api/..."""

    def do_GET(self):
        if self.path.startswith("/api/"):
            self.handle_api("GET")
        else:
            super().do_GET()   # fichiers du front (index.html, app.js...)

    def do_POST(self):
        if self.path.startswith("/api/"):
            self.handle_api("POST")
        else:
            self.send_json({"error": "Route inconnue"}, 404)

    def handle_api(self, method):
        path = urlparse(self.path).path
        try:
            for route_method, pattern, func in ROUTES:
                match = re.fullmatch(pattern, path)
                if match and route_method == method:
                    data, status = func(self.read_body(), *match.groups())
                    self.send_json(data, status)
                    return
            raise ApiError(404, "Route inconnue")
        except ApiError as e:
            self.send_json({"error": e.message}, e.status)
        except Exception as e:
            print(f"[api] erreur sur {method} {path} : {e!r}")
            self.send_json({"error": "Erreur interne du serveur"}, 500)

    def read_body(self):
        """Lit le corps JSON d'une requête POST ({} s'il n'y en a pas)."""
        length = int(self.headers.get("Content-Length") or 0)
        if length == 0:
            return {}
        try:
            body = json.loads(self.rfile.read(length))
        except json.JSONDecodeError:
            raise ApiError(400, "Corps de requête JSON invalide")
        if not isinstance(body, dict):
            raise ApiError(400, "Le corps de la requête doit être un objet JSON")
        return body

    def send_json(self, data, status=200):
        content = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def main():
    # On se place à la racine du projet pour que les chemins de config.json
    # (dossier surveillé, history/) soient relatifs au projet
    os.chdir(ROOT_DIR)
    CONFIG.update(load_config())
    storage.init_storage()
    for folder in CONFIG["watched_folders"]:
        Path(folder).mkdir(parents=True, exist_ok=True)

    # Surveillance automatique en arrière-plan (daemon : s'arrête avec le serveur)
    if CONFIG["watched_folders"]:
        watcher = threading.Thread(
            target=versions.watch_loop,
            args=(HISTORY, CONFIG, scanner.scan),
            daemon=True,
        )
        watcher.start()

    handler = partial(Handler, directory=str(FRONTEND_DIR))
    server = ThreadingHTTPServer((CONFIG["host"], CONFIG["port"]), handler)

    print(f"Serveur lancé sur http://{CONFIG['host']}:{CONFIG['port']}", flush=True)
    print("Ctrl+C pour arrêter", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt du serveur")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
