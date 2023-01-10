Description des graphiques ci-joints :

(1) Nombre de mots - Algo Naïf : la distribution de tailles des mots dans une liste de mots en sortie de l'algorithme Naïf 3D, avec pour comparaison les données pour un texte générique, et modélisé par une distribution exponentielle décroissante (loi à absence de mémoire, avec un paramètre lambda ≈ 0.15)

(2) Nombre de mots - Algo Amélioré : même idée, cette fois avec l'algorithme Amélioré 4D, et modélisé par une loi normale (avec une moyenne vers 9.8, ce qui coïncide aux données en entrée).

(3) Comparaison Naïf vs Amélioré : les légendes sont manquantes pour ce graphiques, mais les grandeurs en abscisse et ordonnées sont identiques (à savoir probabilité par taille de mots). On voit clairement là que la prise en compte de la position dans le mot (donc la mémoire) est cruciale pour avoir un rendu final proche de l'entrée (de distribution normale dans ce cas).

(4) Nombre de mots - Pokémon : les noms de Pokémon forment un bon corpus de mots, car ils sont bien normalement distribués (contrairement à un texte par ex), de variance en taille plutôt faible, et donnent des résultats amusants. On voit encore ici que l'algorithme Amélioré donne en sortie une liste qui coïncide en moyenne et écart-type avec celle en entrée.

(5) Récursion avec Distance de Levenshtein : le but de l'algorithme de récursion est de quantifier la variation de la variabilité au sein des listes de mots créées par l'algorithme Amélioré à mesure que l'on itère le processus. On utilise la distance de Levenshtein pour comparer les éléments entre eux. 
Exactement, ce qui est représenté ici c'est le moyenne de la distance de Levenshtein au premier élément de la liste de mots (de 1000 éléments) en fonction du nombre d'itération (jusqu'à 1000). On a également appliqué une moyenne glissante de taille 30 (≈√1000) pour y voir plus clair, ce qui explique que les discontinuités aux bords.

(6) Récursion avec np.unique() : même idée que dans le cas précédent, mais cette fois en regardant la longueur du vecteur np.unique() de la liste en sortie à chaque itération. Cette méthode est plus exacte que la précédente, en plus d'être asymptotiquement plus avantageuse. On constate alors que la réduction en complexité est drastique, même avec une échelle en loglog de la taille. Cette réduction est constatable dans le document 'pokemon_rec_1000_1.txt' dans le dossier parent, où l'on voit que seuls trois mots différents ont "survécu" au processus itératif.

 