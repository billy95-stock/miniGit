# VersionHub

Gestionnaire de versions automatisé de dossiers, avec une interface web locale.
Projet universitaire — Licence 3 Informatique.

---

## 1. Présentation

VersionHub surveille un ou plusieurs dossiers locaux et enregistre automatiquement leurs versions successives. Dès qu'un dossier est modifié puis reste stable pendant quelques secondes, l'application crée un **snapshot** (une copie de son état). L'utilisateur peut ensuite parcourir l'historique, explorer le contenu des anciennes versions et restaurer celle de son choix, le tout depuis son navigateur.

Contrairement à Git, aucune commande manuelle n'est nécessaire : la sauvegarde des versions est entièrement automatique.

## 2. Objectifs

- Comprendre et mettre en œuvre les principes de base d'un système de gestion de versions.
- Détecter les modifications de fichiers de façon fiable grâce au hachage cryptographique.
- Construire un serveur HTTP et une API sans framework, avec la bibliothèque standard de Python.
- Développer une interface web simple en HTML, CSS et JavaScript.
- Organiser un projet en modules clairs et travailler à plusieurs sur une même base de code.

## 3. Fonctionnalités prévues

- **Ajout de dossiers** : enregistrer des dossiers locaux à surveiller.
- **Détection des changements** : identifier les fichiers ajoutés, modifiés et supprimés.
- **Surveillance périodique** : vérifier les dossiers à intervalle régulier.
- **Snapshot automatique** : créer une version après **5 secondes sans modification**.
- **Historique** : consulter la liste des versions depuis l'interface web.
- **Exploration** : parcourir les fichiers contenus dans une ancienne version.
- **Restauration** : remettre un dossier dans l'état d'une version précédente.

## 4. Technologies utilisées

| Technologie | Usage |
|---|---|
| Python 3 (bibliothèque standard uniquement) | Backend |
| `http.server` | Serveur HTTP local et API |
| `hashlib` (SHA-256) | Détection des modifications de fichiers |
| JSON (`json`) | Stockage des métadonnées |
| HTML | Structure de l'interface |
| CSS | Mise en forme de l'interface |
| JavaScript | Interactions avec le backend |

Aucun framework (ni Flask, ni FastAPI) et aucune dépendance externe.

## 5. Architecture du projet

```text
miniGit/
│
├── backend/
│   ├── main.py        # Point d'entrée : lance le serveur HTTP et définit les routes de l'API
│   ├── scanner.py     # Parcourt les dossiers surveillés et calcule l'empreinte SHA-256 des fichiers
│   ├── versions.py    # Compare les états, crée les snapshots, liste et restaure les versions
│   └── storage.py     # Lit et écrit les métadonnées JSON et les copies de fichiers dans history/
│
├── frontend/
│   ├── index.html     # Structure de l'interface web
│   ├── style.css      # Design de l'interface
│   └── app.js         # Appels à l'API et mise à jour de l'affichage
│
├── history/           # Snapshots et métadonnées générés par l'application
│
├── requirements.txt   # Vide : aucune dépendance externe
├── Makefile           # Commande de lancement (make run)
└── README.md          # Documentation du projet
```

## 6. Fonctionnement général

1. **Enregistrement** : l'utilisateur ajoute un dossier depuis l'interface web. Le chemin est mémorisé dans un fichier JSON.
2. **Scan** : à intervalle régulier, `scanner.py` parcourt chaque dossier surveillé et calcule l'empreinte SHA-256 de chaque fichier.
3. **Comparaison** : `versions.py` compare ces empreintes avec celles du dernier état connu pour déterminer les fichiers ajoutés, modifiés et supprimés.
4. **Stabilisation** : lorsqu'un changement est détecté, l'application attend que le dossier reste inchangé pendant 5 secondes, afin d'éviter de créer une version au milieu d'une série de modifications.
5. **Snapshot** : une nouvelle version est créée. `storage.py` copie les fichiers dans `history/` et enregistre les métadonnées (date, liste des fichiers, empreintes, changements) au format JSON.
6. **Consultation** : le frontend interroge l'API exposée par `main.py` pour afficher l'historique, explorer une version ou demander une restauration.
7. **Restauration** : les fichiers de la version choisie sont recopiés depuis `history/` vers le dossier surveillé.

```text
Navigateur (HTML/CSS/JS)  <──HTTP/JSON──>  main.py (http.server)
                                              │
                          scanner.py ──> versions.py ──> storage.py ──> history/
```

## 7. Installation et lancement (prévus)

Prérequis : Python 3 et `make`.

```bash
cd miniGit
make run
```

La commande `make run` exécute `python3 backend/main.py`. L'interface sera ensuite accessible dans le navigateur à l'adresse locale affichée par le serveur (par exemple `http://localhost:8000`).

Aucune installation de paquet n'est nécessaire.

## 8. Répartition possible du travail (4 étudiants)

| Étudiant | Responsabilité | Fichiers principaux |
|---|---|---|
| Étudiant 1 | Serveur HTTP et API (routes, réponses JSON, service des fichiers du frontend) | `backend/main.py` |
| Étudiant 2 | Scan des dossiers, hachage SHA-256, détection des ajouts/modifications/suppressions | `backend/scanner.py` |
| Étudiant 3 | Gestion des versions : délai de 5 s, création des snapshots, stockage JSON, restauration | `backend/versions.py`, `backend/storage.py` |
| Étudiant 4 | Interface web : affichage des dossiers, de l'historique, exploration et restauration | `frontend/index.html`, `frontend/style.css`, `frontend/app.js` |

Conseil : définir ensemble, dès le début, le format des métadonnées JSON et la liste des routes de l'API, afin que chacun puisse avancer en parallèle.
