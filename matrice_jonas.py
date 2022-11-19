import numpy as np
import random as rd

with open('mots_francais.txt','r',-1,'utf-8') as mots:
    MOTS = ''
    letters = []
    ldico = {}
    mat_size = 50
    mat = np.zeros((mat_size,mat_size),dtype='int32')
    proba = np.zeros((mat_size,mat_size)) #,dtype='float32')
    
    for m in mots: MOTS += (m[:-2].lower()+' ')
    
    l_i = MOTS[0]
    letters.append(l_i)
    ldico[l_i] = 1
    i = letters.index(l_i)
    for k in range(len(MOTS)-1):
        l_j = l_i
        l_i = MOTS[k+1]
        if l_i not in letters:
            letters.append(l_i)
            ldico[l_i] = 0
        j = i
        i = letters.index(l_i)
        ldico[l_j] += 1
        mat[i,j] += 1
    
    alpha = len(letters)

    div = lambda x,a : x/a # version itérative de calculer p mais ça somme pas à 1
    vdiv = np.vectorize(div)
    for i in range(mat_size):
        try: proba[i] = vdiv(mat[i],ldico[letters[i]])
        except: pass

    s=mat.sum(axis=1) # version vectorielle qui marche
    st=np.tile(s.T,(mat_size,1)).T
    p=mat.astype('float')/st
    p[np.isnan(p)]=0
    
    text = ' '
    for _ in range(100): text = np.random.choice(letters,p=p[letters.index(text[0])][:alpha]) + text

    print(text)

            

    