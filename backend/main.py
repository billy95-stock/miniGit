"""Point d'entrée : serveur HTTP local (http.server) et routes de l'API."""

import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

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


class Handler(SimpleHTTPRequestHandler):
    """Sert les fichiers du dossier frontend/.
    Les routes /api/... seront ajoutées à l'étape 2."""


def main():
    config = load_config()
    handler = partial(Handler, directory=str(FRONTEND_DIR))
    server = ThreadingHTTPServer((config["host"], config["port"]), handler)

    print(f"Serveur lancé sur http://{config['host']}:{config['port']}")
    print("Ctrl+C pour arrêter")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt du serveur")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
