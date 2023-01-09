## Dans ce code le but est de tester comment le code 'amélioré' résiste à l'utilisation itérée, 
## cad on donne en entrée au code 'amélioré' ce qu'il vient de produire en sortie.
## C'est également une version exclusivement fonctionnelle du programme 'amélioré"

# cette fonction permet d'ouvrir un document texte et le rendre facilement exploitable, et renvoie une liste de mots
def debut(texte):
    import codecs,unicodedata
    import os
    local_path = os.path.dirname(__file__)

    lmot=[]
    with codecs.open(local_path + '/../Data/' + texte, 'r', encoding='utf-8') as mots:
            for l in mots:
                l = l.lower()
                nk = unicodedata.normalize('NFKD', l)
                mot = nk.encode('ASCII', 'ignore') # enlever les accents
                lmot.append(str(mot)[2:-2])
    return(lmot)
    
# création d'un dictionnaire des listes de mots par taille
def mdico(texte):
    
    dico = {}
    for mot in debut(texte):
        if len(mot) in dico.keys():
            dico[len(mot)].append(mot)
        else:
            dico[len(mot)] = [mot]
    return dico


# fonction qui va donner le numéro d'une lettre
def id(lettre):
    return ord(lettre) - 97

# fonction qui donne la lettre associée à un numéro
def di(indice):
    return chr(indice + 97)

# fonction qui crée la matrice de probabilités à l'aide des fonctions créées précédemment
def proba(texte):
    global lmot
    nb_lettre = 26
    lg_max = max(mdico(texte).keys())


    # initialisation de la matrice des probas
    mat = [[[[0 for p in range(nb_lettre + 1)] for k in range(lg_max)] for i in range(nb_lettre + 1)]for j in range(nb_lettre + 1)]

    # comptage 
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
            mat[-1][-1][0][id(mot[0])] += 1 # proba de la première lettre
            if L >= 2:
                mat[-1][id(mot[0])][0][id(mot[1])] += 1 # proba de la deuxième lettre
                for i in range(1, L-2):
                    mat[id(mot[i-1])][id(mot[i])][i][id(mot[i+1])] += 1 # proba de lettre suivant la i-eme lettre
                mat[id(mot[L-2])][id(mot[L-1])][L-1][-1] += 1 # proba d'être la dernière lettre
            if L == 1:
                mat[-1][id(mot[0])][0][-1] += 1

    # division pour obtenir des probas
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


# creation de la prochaine lettre, étant données les deux précédentes et la position dans le mot
def next_l(*l_1, pos = 0): # l_1 tuple qui contient (l-1, l)
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
        
# fonction qui crée un mot
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

# fonction qui crée le nombre de mots désiré et les enregistre dans un document .txt au nom 'out'
# (le booléen strip est utilisé dans le cas récursif, pour éviter un problème de troncature progressive de la fin des mots)
def create_words(texte,n,out='charabia_ameliore.txt',strip=False):
    import os 
    local_path = os.path.dirname(__file__)

    global lmot,mat
    lmot = debut(texte)
    mat = proba(texte)
    charabia = open(local_path + '/../Resultats/' + out, 'w')
    for i in range(n):
        word = create_word()
        if strip: word = word.replace('{','')
        charabia.writelines(word)
        charabia.writelines('\n')
    charabia.close()

# fonction finale qui itère le procédé de création des mots de n mots, elle crée k documents .txt qu'elle 
# supprime au fur et à mesure et garde la k-ème
def recursive_words(texte,n,k):
    import os
    local_path = os.path.dirname(__file__)

    nom = local_path + '/../Resultats/' + texte[:-5]
    rec_nom = local_path + '/../Resultats/'
    texte_out = 'rec_0.txt'
    create_words(texte,n,out=texte_out)
    for j in range(k-1):
        create_words(f'/../Resultats/rec_{j}.txt',n,out = f'rec_{j+1}.txt')
        os.remove(rec_nom + f'rec_{j}.txt')
    if os.path.exists(nom + f'rec_{k}.txt'):
        m = 1
        while os.path.exists(nom + f'rec_{k}_{m}.txt'):
            m += 1
        create_words(f'/../Resultats/rec_{k-1}.txt',n,out = texte[:-5] + f'rec_{k}_{m}.txt',strip=True)
    else : create_words(f'/../Resultats/rec_{k-1}.txt',n,out = texte[:-5] + f'rec_{k}.txt',strip=True)
    os.remove(rec_nom + f'rec_{k-1}.txt')

def rec_stat(texte,n,k):
    import os,sys,math
    import matplotlib.pyplot as plt
    import numpy as np

    local_path = os.path.dirname(__file__)

    # /!\ le texte source doit se trouver dans le dossier 'Data'
    sys.path.append(local_path + '/../Data/' + texte)

    from moy_glissante import moy_glis,lissage_2
    from edition_texte import wlist

    X = [i for i in range(k+1)]
    nbr_mots_differents = []
    
    texte_out = 'rec_0.txt'
    create_words(texte,n,out=texte_out)
    W = wlist(texte_out)
    nbr_mots_differents.append(len(np.unique(np.array(W))))

    for j in range(k):
        texte_out = f'rec_{j+1}.txt'
        create_words(f'rec_{j}.txt',n,out = texte_out)
        W = wlist(texte_out)
        nbr_mots_differents.append(len(np.unique(np.array(W))))
    os.remove(f'rec_{k}.txt')

    plt.plot(X,nbr_mots_differents)
    plt.show()
            

recursive_words('mots_francais.txt',1000,100)

