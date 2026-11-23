import shutil
from pathlib import Path
import json

HISTORY_DIR = Path(__file__).resolve().parent.parent / "history"


def init_storage():
    """Crée le dossier history s'il n'existe pas."""
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    return HISTORY_DIR


def create_snapshot(number, source_dir, changes):
    """Copie les fichiers ajoutés et modifiés dans un snapshot."""

    snapshot_dir = HISTORY_DIR / f"snapshot_{number:03d}"
    files_dir = snapshot_dir / "files"

    files_dir.mkdir(parents=True, exist_ok=True)

    files_to_copy = changes["added"] + changes["modified"]

    for file_path in files_to_copy:
        source = Path(file_path)

        if source.is_file():
            relative_path = source.relative_to(source_dir)
            destination = files_dir / relative_path

            destination.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(source, destination)

    return snapshot_dir

def save_metadata(version):
    """Enregistre les informations d'une version dans un fichier JSON."""

    snapshot_dir = HISTORY_DIR / f"snapshot_{version['number']:03d}"
    fichier = snapshot_dir / "metadata.json"

    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(version, f, indent=4, ensure_ascii=False)
    