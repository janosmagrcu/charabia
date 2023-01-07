def words_jonas(url,n=1): #si on spécifie pas, ça crée un seul mot, sinon c'est en fonction du nombre de lettres :(
    import numpy as np
    import random as rd

    with open(url,'r') as mots:
        MOTS = ''
        letters = []
        mat_size = 71
        mat = np.zeros((mat_size,mat_size,mat_size))

        for m in mots: MOTS += (m[:-1].lower()+' ')
        
        l_i = MOTS[1]
        l_j = MOTS[0]
        letters.append(l_j)
        if l_i not in letters: letters.append(l_i)
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

        
        nb_letters = len(letters)
        #print(mat.sum(axis=(0,1,2)))
        
        mat_r = np.zeros((nb_letters,nb_letters,nb_letters))
        for i in range(nb_letters):
            for j in range(nb_letters):
                for k in range(nb_letters):
                    mat_r[i,j,k] = mat[i,j,k]

        '''

        s = mat_r.sum(axis=1)
        st = np.tile(s.T,(nb_letters,1,1)).T

        zeros = np.where(st==0)[0]
        #print(zeros)

        p = mat_r.astype('float')
        p[np.isnan(p)] = 0
        np.divide(p,st,where=(st!=0))

        text = 'e '
        for _ in range(n): text = np.random.choice(letters,p=p[letters.index(text[1]),letters.index(text[0])]) + text
        l = ''
        while l != ' ':
            l = np.random.choice(letters,p=p[letters.index(text[1]),letters.index(text[0])])
            text = l + text
        text = text.replace(' ','\n')

        '''

        text = 'e '
        for _ in range(n): 
            text = rd.choices(letters,weights=mat_r[letters.index(text[1]),letters.index(text[0]),:])[0] + text
        l = ''
        while l != ' ':
            l = rd.choices(letters,weights=mat_r[letters.index(text[1]),letters.index(text[0]),:])[0]
            text = l + text
        text = text.replace(' ','\n')

    with open(url[:-5]+'jonas.txt','x') as lines:
        lines.write(text)
