
"""Lecture/écriture des métadonnées JSON et des fichiers dans history/."""

from pathlib import Path

HISTORY_DIR = Path(__file__).resolve().parent.parent / "history"


def init_storage():
    """Crée le dossier history s'il n'existe pas."""
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    return HISTORY_DIR