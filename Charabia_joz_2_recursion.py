def debut(url):
    import codecs,unicodedata

    lmot=[]
    with codecs.open(url, 'r', encoding='utf-8') as mots:
            for l in mots:
                l = l.lower()
                nk = unicodedata.normalize('NFKD', l)
                mot = nk.encode('ASCII', 'ignore') #enlever les accents
                lmot.append(str(mot)[2:-2])
    return(lmot)
    

def mdico(url):
    #création d'un dictionnaire des listes de mots par taille
    dico = {}
    for mot in debut(url):
        if len(mot) in dico.keys():
            dico[len(mot)].append(mot)
        else:
            dico[len(mot)] = [mot]
    return dico


#fonction qui va donner le numéro d'une lettre
def id(lettre):
    return ord(lettre) - 97

def di(indice):
    return chr(indice + 97)

def proba(url):
    global lmot
    nb_lettre = 26
    #nb_mot = int(len(lmot))
    lg_max = max(mdico(url).keys())
    #consonnes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v',  'w', 'x', 'z']
    #voyelles = ['a', 'e', 'i', 'o', 'u', 'y']



    #initialisation de la matrice des probas
    mat = [[[[0 for p in range(nb_lettre + 1)] for k in range(lg_max)] for i in range(nb_lettre + 1)]for j in range(nb_lettre + 1)]

    #comptage 
    for mot in lmot:
        if len(mot) == 0: continue
        if '-' in mot:
            t_ = mot.index('-')
            mot1 = mot[:t_]
            mot2 = mot[t_+1:]
            lmot.append(mot1)
            lmot.append(mot2)
        else:
            L = len(mot)
            mat[-1][-1][0][id(mot[0])] += 1 #proba de la première lettre
            if L >= 2:
                mat[-1][id(mot[0])][0][id(mot[1])] += 1 #proba de la deuxième lettre
                for i in range(1, L-2):
                    mat[id(mot[i-1])][id(mot[i])][i][id(mot[i+1])] += 1 #proba de lettre suivant la i-eme lettre
                mat[id(mot[L-2])][id(mot[L-1])][L-1][-1] += 1 #proba d'être la dernière lettre
            if L == 1:
                pass #mat[-1][id(mot[0])][0][-1] += 1  ## faut retirer les mots de 1 lettre ??

    #division pour obtenir des probas

    for i in range(nb_lettre + 1):
        for j in range(nb_lettre + 1):
            for k in range(lg_max):
                s = 0
                for p in range(nb_lettre + 1):
                    s += mat[i][j][k][p]
                if s != 0:
                    for p in range(nb_lettre + 1):
                        mat[i][j][k][p] /= s
    return mat


#creation de mots
def next_l(*l_1, pos = 0): #l_1 tuple qui contient (l-1, l)
    import random
    nb_lettre = 26
    global mat 
    liste_lettres = [di(k) for k in range(nb_lettre + 1)]
    if len(l_1) == 0:
        return (random.choices(liste_lettres, weights = mat[-1][-1][pos]))[0]
    if len(l_1) == 1:
        return (random.choices(liste_lettres, weights = mat[-1][id(l_1[0])][pos]))[0]
    if len(l_1) == 2:
        try:
            prob = (random.choices(liste_lettres, weights = mat[id(l_1[0])][id(l_1[1])][pos]))[0]
            return prob
        except:
            return '{'
        #return (random.choices(liste_lettres, weights = mat[id(l_1[0])][id(l_1[1])][pos]))[0]

def create_word():
    lettre1 = next_l()
    while lettre1 == '{':
        lettre1 = next_l()
    lettre2 = next_l(lettre1)
    if lettre2 == '{':
        return lettre1
    u = 2
    mot = lettre1 + lettre2
    while lettre2 != '{':
        lettre = next_l(lettre1, lettre2, pos = u-1)
        mot += lettre
        lettre1, lettre2 = lettre2, lettre
        u += 1
    return mot


def create_words(url,n,out='charabia.txt',strip=True):
    global lmot,mat
    lmot = debut(url)
    mat = proba(url)
    charabia = open(out, 'w')
    for i in range(n):
        word = create_word()
        if strip: word = word.replace('{','')
        charabia.writelines(word)
        charabia.writelines('\n')
    charabia.close()


def recursive_words(url,n,k):
    import os
    nom = url[:-5]
    url_out = 'rec_0.txt'
    create_words(url,n,out=url_out,strip=False)
    for j in range(k-1):
        create_words(f'rec_{j}.txt',n,out = f'rec_{j+1}.txt',strip=False)
        os.remove(f'rec_{j}.txt')
    if os.path.exists(nom + f'rec_{k}.txt'):
        m = 1
        while os.path.exists(nom + f'rec_{k}_{m}.txt'):
            m += 1
        create_words(f'rec_{k-1}.txt',n,out = (nom + f'rec_{k}_{m}.txt'))
    else : create_words(f'rec_{k-1}.txt',n,out = (nom + f'rec_{k}.txt'))
    os.remove(f'rec_{k-1}.txt')

def rec_stat(url,n,k):
    import os,sys,math
    import matplotlib.pyplot as plt
    import numpy as np
    #import scipy.special as spe
    sys.path.append('/Users/jonas/Desktop/Cours/Info/projet')
    sys.path.append('/Users/jonas/Desktop/Cours/Info/projet/Stats')
    sys.path.append('/users/jonas/Desktop/Cours/Info')
    from moy_glissante import moy_glis,lissage_2
    from levenshtein import levenshtein
    from edition_texte import wlist

    X = [i for i in range(k+1)]
    nbr_mots_differents = []
    
    url_out = 'rec_0.txt'
    create_words(url,n,out=url_out)
    W = wlist(url_out)
    ref = W[1]
    nbr_mots_differents.append(len(np.unique(np.array(W))))

    for j in range(k):
        url_out = f'rec_{j+1}.txt'
        create_words(f'rec_{j}.txt',n,out = url_out)
        W = wlist(url_out)
        ref = W[1]
        nbr_mots_differents.append(len(np.unique(np.array(W))))
    os.remove(f'rec_{k}.txt')

    #bord = int(math.sqrt(k))
    #Y = lissage_2(Lev,bord)[bord:-1*bord]
    nbr_mots_differents_log = [math.log(nbr) for nbr in nbr_mots_differents]
    plt.plot(X,nbr_mots_differents)
    #plt.plot(X[bord:-1*bord],Y,'r')
    plt.show()
            


def create_verbs(n):
    liste_term_troisieme_groupe = ['bre', 'cre', 'dre', 'fre', 'gre', 'hre', 'jre', 'kre', 'lre', 'mre', 'nre', 'pre', 'qre', 'rre', 'sre', 'tre', 'vre', 'wre', 'xre', 'zre', 'ire']
    charabia = open('verbs_charabia.txt', 'w')
    for i in range(n):
        mot = create_word()
        while mot[-2:] not in ['er', 'ir'] and mot[-3:] not in liste_term_troisieme_groupe:
            mot = create_word()
        charabia.writelines(mot)
        charabia.writelines('\n')
    charabia.close()


