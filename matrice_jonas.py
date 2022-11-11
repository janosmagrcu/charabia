with open('mots_francais.txt','r',-1,'utf-8') as mots:
    MOTS = ''
    letters = []
    for m in mots: MOTS += (m[:-2]+' ')
    for l in MOTS:
        if l not in letters: letters.append(l)
    alpha = len(letters)
    mat = [[0]*alpha]*alpha
    for k in range(len(MOTS)-1):
        i = letters.index(MOTS[k+1])
        j = letters.index(MOTS[k])
        mat[i][j] += 1 # pk ca marche pas ??

    print(mat)




            

    