import os, codecs

local_path = os.path.dirname(__file__)
file_path = os.path.join(local_path, "Data/liste.de.mots.francais.frgut.txt")


with codecs.open(file_path, "r", "utf-8") as fichier_mots:

    # nettoyage fichier_mots :
    string_mots = ' '.join(fichier_mots.readlines()).replace('\n','').lower()
    # Problème avant car str(fichier_mots) = <codecs.StreamReaderWriter object at 0x0000029ED948FF70>

    characteres = sorted(set(string_mots))
    print(characteres)

taille_characteres = tc = len(characteres)
M = [[0] * tc for i in range(tc)]

for i, char in enumerate(characteres):
    n_occur = 0
    for i2, char2 in enumerate(characteres):
        if i2 < len(characteres) - 1 and char == char2:
            n_occur += 1
            M[i][characteres.index(characteres[i2 + 1])] += 1
    for j in range(len(characteres)):
        if n_occur != 0:
            j = int(j)
            M[i][j] = (M[i][j] / n_occur)  # Pour que M ne contienne que des 0 et des 1

for i in range(len(characteres)):
    print(M[i])