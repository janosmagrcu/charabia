import numpy as np

with open('mots_francais.txt','r',-1,'utf-8') as mots:
    MOTS = ''
    letters = []
    mat_size = 42
    mat = np.zeros((mat_size,mat_size,mat_size),dtype='int32')
    
    for m in mots: MOTS += (m[:-2].lower()+' ')
    
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

    s=mat.sum(axis=2)
    st=np.tile(s.T,(mat_size,1,1)).T
    try: p=mat.astype('float')/st
    except: RuntimeWarning
    p[np.isnan(p)]=0
    
    text = 'e .'
    for _ in range(200): text = np.random.choice(letters,p=p[letters.index(text[1]),letters.index(text[0])]) + text
    l = ''
    while l != ' ':
        l = np.random.choice(letters,p=p[letters.index(text[1]),letters.index(text[0])])
        text = l + text
    imaj = letters.index(text[1])
    text = letters[imaj].upper() + text[2:]
    print(text)
    