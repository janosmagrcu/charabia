## Ceci est la version 2D du créateur de pseudo-mots avec une chaîne de Markov, à partir de la liste des mots français présente dans Data.

## Ce code est très lent car il utilise la fonction np.random.choices qui n'est pas optimale, et les résultats sont plutôt décevants.

import numpy as np
import os
local_path = os.path.dirname(__file__)

with open(local_path + '/../Data/mots_francais.txt','r',-1,'utf-8') as mots:
    MOTS = ''
    letters = []
    ldico = {}
    mat_size = 50
    mat = np.zeros((mat_size,mat_size),dtype='int32')
    
    
    for m in mots: MOTS += (m[:-2].lower()+' ')
    
    # on remplit la matrice de probas
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

    '''
    # version itérative pour calculer p mais ça somme pas à 1
    proba = np.zeros((mat_size,mat_size))
    div = lambda x,a : x/a 
    vdiv = np.vectorize(div)
    for i in range(mat_size):
        try: proba[i] = vdiv(mat[i],ldico[letters[i]])
        except: pass
    '''

    # version vectorielle qui marche
    s=mat.sum(axis=1)
    st=np.tile(s.T,(mat_size,1)).T
    p=mat.astype('float')/st 
    p[np.isnan(p)]=0 # il y a quand même des zéros qui doivent se faufiler mais je sais pas où
    

    # on initialise le texte à une espace et on en déduit les lettres précédentes (l'espace est une lettre)
    text = ' '
    for _ in range(100): text = np.random.choice(letters,p=p[letters.index(text[0])][:alpha]) + text

    # le résultat est directement écrit dans le shell
    print(text)


            

    