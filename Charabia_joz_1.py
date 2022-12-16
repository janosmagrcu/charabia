import codecs
import unicodedata
import random

lmot = []

#traitement de la liste de mot en liste python
with codecs.open('Liste mot.txt', 'r', encoding='utf-8') as mots:
    for l in mots:
        l = l.lower()
        nk = unicodedata.normalize('NFKD', l[:-2])
        mot = nk.encode('ASCII', 'ignore') #enlever les accents
        lmot.append(str(mot)[2:-1])
    
        #lmot.append(l[:-2])

#création d'un dictionnaire des listes de mots par taille
dico = {}
for mot in lmot:
    if len(mot) in dico.keys():
        dico[len(mot)].append(mot)
    else:
        dico[len(mot)] = [mot]


#fonction qui va donner le numéro d'une lettre
def id(lettre):
    n = ord(lettre) - 97
    return n

def di(indice):
    return chr(indice + 97)

nb_lettre = 26
nb_mot = int(len(lmot))
lg_max = len(dico.keys())
liste_lettres = [di(k) for k in range(nb_lettre + 1)]
consonnes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v',  'w', 'x', 'z']
voyelles = ['a', 'e', 'i', 'o', 'u', 'y']
liste_term_troisieme_groupe = ['bre', 'cre', 'dre', 'fre', 'gre', 'hre', 'jre', 'kre', 'lre', 'mre', 'nre', 'pre', 'qre', 'rre', 'sre', 'tre', 'vre', 'wre', 'xre', 'zre', 'ire']


#initialisation de la matrice des probas
mat = [[[[0 for p in range(nb_lettre + 1)] for k in range(lg_max)] for i in range(nb_lettre + 1)]for j in range(nb_lettre + 1)]

#comptage 
for mot in lmot:
    if '-' in mot:
        t_ = mot.index('-')
        mot1 = mot[:t_]
        mot2 = mot[t_+1:]
        lmot.append(mot1)
        lmot.append(mot2)
    else:
        n = len(mot)
        mat[-1][-1][0][id(mot[0])] += 1 #proba de la première lettre
        if n >= 2:
            mat[-1][id(mot[0])][0][id(mot[1])] += 1 #proba de la deuxième lettre
            for i in range(1, n-2):
                mat[id(mot[i-1])][id(mot[i])][i][id(mot[i+1])] += 1 #proba de lettre suivant la i-eme lettre
            mat[id(mot[n-2])][id(mot[n-1])][n-1][-1] += 1 #proba d'être la dernière lettre
        if n == 1:
            mat[-1][id(mot[0])][0][-1] += 1

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

#creation de mots
def next_l(*l_1, pos = 0): #l_1 tuple qui contient (l-1, l)
    global liste_lettres
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
    n = 2
    mot = lettre1 + lettre2
    while lettre2 != '{':
        lettre = next_l(lettre1, lettre2, pos = n-1)
        mot += lettre
        lettre1, lettre2 = lettre2, lettre
        n += 1
    return mot[:-1]


def create_words(n):
    charabia = open('charabia.txt', 'w')
    for i in range(n):
        charabia.writelines(create_word())
        charabia.writelines('\n')
    charabia.close()

def create_verbs(n):
    charabia = open('verbs_charabia.txt', 'w')
    for i in range(n):
        mot = create_word()
        while mot[-2:] not in ['er', 'ir'] and mot[-3:] not in liste_term_troisieme_groupe:
            mot = create_word()
        charabia.writelines(mot)
        charabia.writelines('\n')
    charabia.close()
'''
texte = open('livre.txt', 'w')  
for l in texte:

def petit_mot(txt):
    txt = txt.split()
    mot_diff = []
    occurences_mots = []
    for mot in txt:
        if mot not in mot_diff:
            mot_diff.append(mot)
    for mot in mot_diff:
        occurences_mots.append(txt.count(mot))
'''

print(create_words(2000))
