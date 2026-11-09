# miniGit

Groupe gestionnaire de version automatisé : HAMMOUCHE Sami, BOUKHLLIA Elias, HAMARA Camara, AZEDDIN Bilail

## Description

Un programme en Python qui surveille un dossier et qui sauvegarde automatiquement ses versions quand il est modifié. On peut ensuite voir l'historique des versions et en restaurer une, tout se fait depuis une petite interface web en local

## Partie 1 : fonctionnalités

Noyau minimal :

1. Fichier de configuration (dossier a surveiller, fréquence de vérification, temps d'attente avant une sauvegarde auto, dossier des sauvegardes)
2. Détecter les fichiers ajoutés modifiés et supprimés
   - dépend de 1
3. Créer une version avec un numéro et une date, seulement si quelque chose a changé
   - dépend de 2
4. Sauvegarde automatique et sauvegarde manuelle. la sauvegarde automatique se fait quand le dossier a pas été modifié pendant un certain temps pour pas créer une version au milieu de plusieurs modifications. Ce temps est réglable dans la config et la valeur par défaut est encore a décider
   - dépend de 3
5. Afficher l'historique des versions
   - dépend de 3
6. Restaurer une version dans le dossier d'origine ou dans un autre dossier
   - dépend de 5

Fonctionnalités en plus :

7. Interface web
   - dépend de 4, 5 et 6
8. Explorer les fichiers d'une ancienne version sans devoir la restaurer
   - dépend de 5
9. Télécharger une version en .zip
   - dépend de 5
10. Voir les differences entre deux versions d'un fichier
    - dépend de 5
11. Ignorer certains fichiers (ex les fichiers temporaires) avec un fichier .ignore comme le .gitignore
    - dépend de 2
12. Garder un journal de ce que fait le programme (versions créées, restaurations, erreurs...)
    - dépend de 4
13. Compresser les fichiers sauvegardés pour prendre encore moins de place
    - dépend de 4
14. Une notification sur l'ordi quand une nouvelle version est créée
    - dépend de 4
15. Afficher le code en couleur quand on explore une ancienne version
    - dépend de 8
16. Pouvoir utiliser le programme depuis le terminal (sauvegarder, lister, restaurer) sans passer par l'interface web
    - dépend de 4, 5 et 6

Priorités : d'abord 1 à 6, ensuite 7 et 8 et apres 9 à 16 si on a le temps.

## Partie 2 : modules

On utilise surtout la bibliothèque standard de Python donc presque rien a installer. Ces modules marchent sous Windows et Linux, ils sont maintenus par l'équipe officielle de Python et la documentation est complète sur docs.python.org

- json : pour la configuration et l'historique des versions.
- pathlib : pour parcourir les dossiers et lister les fichiers d'une ancienne version
- hashlib : pour savoir si un fichier a changé grace a son empreinte SHA-256. C'est plus fiable que la date de modification qui peut changer alors que le contenu est le même. Par contre il dit juste si le fichier a changé mais pas ce qui a changé (c'est difflib qui fait ca).
- shutil : pour copier les fichiers quand on sauvegarde ou qu'on restaure. Pour prendre moins de place on recopie pas les fichiers qui ont pas changé
- time et threading : pour vérifier le dossier régulièrement et attendre un certain temps sans modification avant de sauvegarder. La fréquence et le temps d'attente sont paramétrables dans la config, la durée par défaut est encore a décider. On a regardé le module watchdog mais il faut l'installer et une simple boucle suffit.
- http.server : pour le serveur web. Il est pas fait pour un vrai site en ligne mais pour un petit outil en local ça suffit, Flask est plus pratique mais faut l'installer
- zipfile (optionnel) : pour télécharger une version en .zip
- difflib (optionnel) : pour afficher les différences entre deux fichiers. Ca marche que pour les fichiers texte, pas pour les images par exemple.
- fnmatch (optionnel) : pour reconnaitre les fichiers a ignorer avec des règles comme *.tmp
- logging (optionnel) : pour écrire le journal du programme dans un fichier, c'est mieux que des print car on peut choisir le niveau (info, erreur)
- zlib (optionnel) : pour compresser les fichiers sauvegardés. Ca sert pas a grand chose sur des fichiers deja compressés comme les images ou les .zip
- argparse (optionnel) : pour lancer des commandes dans le terminal, par exemple python main.py save ou python main.py restore 3. Il crée aussi une aide tout seul avec --help, c'est pratique pour tester le programme avant que l'interface web soit prête.

On utilise aussi deux modules externes pour les fonctionnalités en plus :

- plyer (optionnel) : pour les notifications sur Windows et Linux. Il s'installe avec pip et il est simple a utiliser mais il est moins mis a jour que les autres, et sous Linux il faut que le système gère les notifications
- Pygments (optionnel) : pour colorer le code. Il s'installe avec pip, il est très utilisé, bien maintenu et bien documenté. Il reconnait des centaines de langages mais il sert que pour les fichiers de code ou de texte.

watchdog et Flask s'installent facilement avec pip, ils sont bien maintenus avec une grosse communauté et une bonne doc. On les garde de côté si la bibliothèque standard suffit pas.

## Lancement

```
pip install -r requirements.txt
make run
```
