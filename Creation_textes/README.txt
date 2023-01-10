Voici la note d'utilisation de la partie "création de textes" de notre projet.
L'objectif de cette partie est de fabriquer des phrases ayant des des structures grammaticales probables en français. De même que nous fabriquons des pseudo-mots dans "Création de mots", nous fabriquons ici des pseudo-phrases : l'idée est la même, mais nous avons changé d'échelle.

Ce dossier contient 3 codes :

- Préparation_du_lexicon.py : Il nettoie la base de données Lexicon et créé (dans Data) des fichiers pickle contenant des ditionnaire issus de cette base de données.
Il n'est pas nécessaire de faire tourner ce code, les fichiers pickle sont déjà présents dans le repository.

- Analyse_proba_de_corpus.py : Dans ce code, nous faison lire un corpus de livres à notre algorithme pour créer les tables de probabilités de transition des structures grammaticales.
Ce code a une durée d'éxécution assez importante (une vingtaine de minutes ou plus d'une heure selon un des réglages présents du code).
Il n'est donc pas nécessaire que vous l'éxécutiez, toutefois les tables de probabilités étant trop lourdes pour Github, voici un lien wetransfer pour les télécharger :
https://we.tl/t-OSSQl6CbIU (/!\ expire le 17/01) => Il faut ensuite déziper les fichiers et les placer dans Data/Probas

- Générateur_de_phrases.py : Après avoir téléchargé les fichiers du lien, c'est ce code que vous devrez faire tourner pour obtenir les pseudo-phrases !
Pour chaque génération de texte, vous pourrez choisir la profondeur maximale de la table de probabilité utillisée (c'est à dire sur combien de mots précédents se base-t-on pour décider du mot que l'on ajoute), le nombre de phrases à générer, ainsi que l'utilisation de la fréquence des mots ou non (c'est-à-dire favoriser l'utilisation de mots de langage courant ou non).
