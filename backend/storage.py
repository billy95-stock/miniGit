import shutil
from pathlib import Path

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

    