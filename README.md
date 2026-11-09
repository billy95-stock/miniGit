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
