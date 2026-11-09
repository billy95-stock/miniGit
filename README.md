# miniGit

Groupe gestionnaire de version automatisé : HAMMOUCHE Sami, BOUKHLLIA Elias, HAMARA Camara, AZEDDIN Bilail

## Description

Un programme en Python qui surveille un dossier et qui sauvegarde automatiquement ses versions quand il est modifié. On peut ensuite voir l'historique des versions et en restaurer une, tout se fait depuis une petite interface web en local

## Partie 1 : fonctionnalités

Noyau minimal :

1. Fichier de configuration (dossier a surveiller, fréquence de vérification, dossier des sauvegardes)
2. Détecter les fichiers ajoutés modifiés et supprimés
   - dépend de 1
3. Créer une version avec un numéro et une date, seulement si quelque chose a changé
   - dépend de 2
4. Sauvegarde automatique et sauvegarde manuelle. la sauvegarde automatique se fait quand le dossier a pas été modifié pendant 5 secondes pour pas créer une version au milieu de plusieurs modifications
   - dépend de 3
5. Afficher l'historique des versions
   - dépend de 3
6. Restaurer une version dans le dossier d'origine ou dans un autre dossier
   - dépend de 5