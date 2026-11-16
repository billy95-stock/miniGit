"""Scan des dossiers surveillés et calcul des empreintes SHA-256 (hashlib). À implémenter."""


import hashlib
from pathlib import Path

def calculer_empreinte(chemin_fichier):
    sha256_hash = hashlib.sha256()
    try:
        with open(chemin_fichier, "rb") as f:
            for bloc in iter(lambda: f.read(4096), b""):
                sha256_hash.update(bloc)
        return sha256_hash.hexdigest()
    except (OSError, IOError):
        return None
