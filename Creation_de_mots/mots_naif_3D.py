## création de mots avec une matrice de Markov de profondeur 3 qui ne prend pas en compte la position dans le mot => algo "naïf"


def words_naif(texte):
    import numpy as np
    import os

    # /!\ le texte source doit se trouver dans le dossier 'Data/'
    local_path = os.path.dirname(__file__)
    with open(local_path + f'/../Data/{texte}','r',-1,'utf-8') as mots:

        # on initialise la matrice de taille 3 remplies de zéros
        MOTS = ''
        letters = []
        mat_size = 42
        mat = np.zeros((mat_size,mat_size,mat_size),dtype='int32') 

        for m in mots: MOTS += (m[:-2].lower()+' ')

        # on parcourt le texte source pour créer la matrice de probabilités
        l_i = MOTS[1]
        l_j = MOTS[0]
        letters.append(l_j)
        if l_j not in letters: letters.append(l_i)
        i = letters.index(l_i)
        j = letters.index(l_j)
        for u in range(len(MOTS)-2):
            l_k = l_j
            l_j = l_i
            l_i = MOTS[u+2]
            if l_i not in letters:
                letters.append(l_i)
            k = j
            j = i
            i = letters.index(l_i)
            mat[i,j,k] += 1

        alpha = len(letters)

        # on normalise pour avoir les probabilités qui somme à 1
        s=mat.sum(axis=2)
        st=np.tile(s.T,(mat_size,1,1)).T
        try: p=mat.astype('float')/st
        except: RuntimeWarning
        p[np.isnan(p)]=0

        # la suite de mots commence par la fin, on place un 'e' et il va à reculons, on crée 100 000 lettres donc vu la distribution, environ 10 000  mots
        text = 'e '
        for _ in range(100000): text = np.random.choice(letters,p=p[letters.index(text[1]),letters.index(text[0])]) + text
        l = ''
        while l != ' ':
            l = np.random.choice(letters,p=p[letters.index(text[1]),letters.index(text[0])])
            text = l + text
        text = text.replace(' ','\n')

    # on crée les mots dans un fichier texte 'nom_naif_3D.txt'
    with open(local_path + f'/../Resultats/{texte[:-4]}_naif_3D.txt','w',-1,'utf8') as lines:
        lines.write(text)

words_jonas('mots_francais.txt')