characteres = "abcdefghijklmnopqrstuvwxyz "

mots = "manger caca bonjour il comment truc vivant australopitheque fluctuer colon criniere qualifier brouter frousse echelle domino rabin nostalgie charabia"

M = [[0 for i in characteres ] for i in characteres]

for i, char in enumerate(characteres):
    n_occur = 0
    for i2, char2 in enumerate(mots):
        if i2 < len(mots)-1 and char == char2:
            n_occur += 1
            M[i][characteres.index(mots[i2+1])] += 1
    for j in range(len(characteres)):
        if n_occur != 0:
            j = int(j)
            M[i][j] = (M[i][j]/n_occur) # Pour que M ne contienne que des 0 et des 1


for i in range(len(characteres)):
    print(M[i])