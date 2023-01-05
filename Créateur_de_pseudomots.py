import codecs, unicodedata, random, re

#traitement de la liste de mot en liste python
remplacements = {'\x8a': '', '\u202f':' ','\u200b':'','\u2002':' ', '\u2009':' ', '\xad':'','®':'', '‘':"'", 'ý':'y', '©':'', 'ÿ':'y', '⁂':'', '™':'', '“':'"', '»':'"', '  ':' ',"  ":" ", '«': '"', 
    '\t':'', '\n':' ', '\r':' ', '‑':'-', '–':'-', '—':'-', '―':'-', '−':'-', '’':'"', '”':'"', '„':'"', '•':'-'  }
def multi_remplace(texte, remplacements):
    regex = re.compile('|'.join(map(re.escape, remplacements)))
    return regex.sub(lambda match: remplacements[match.group(0)], texte) 


with codecs.open('liste_mot_anglais_triés.txt', "r", "utf-8") as file:
    texte = ''.join(unicodedata.normalize('NFC', line) for line in file.readlines()) 
    texte = multi_remplace(texte, remplacements)
lmot = texte.split()
    


#creation de la liste des "lettres" ou caractères contenus dans les pseudos-mots
d = set()
dmot = set()
lg_max = 0
for mot in lmot:
    if len(mot) > lg_max:
        lg_max = len(mot) #pour trouver la taille du mot le plus long
    dmot.add(mot)
    for c in mot:
        d.add(c)



liste_lettres = list(d)
liste_lettres.remove('-') 
liste_lettres.append('{') #ajout d'un marqueur de fin de mot
print(liste_lettres, len(liste_lettres), lg_max)

# fonction qui associe à chaque "lettre" un nombre
def id(l):
    return liste_lettres.index(l)

#principales variables
nb_lettre = len(liste_lettres)
nb_mot = int(len(lmot))
lg_max = lg_max + 1 #longueur maximale d'un mot
consonnes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v',  'w', 'x', 'z',  'ç']
voyelles = ['a', 'e', 'i', 'o', 'u', 'y', 'é', 'è', 'ê', 'à', 'ù', 'â', 'û', 'ô', 'ä', 'ï', 'ë', 'ü', 'ö', 'î']
liste_term_troisieme_groupe = ['bre', 'cre', 'dre', 'fre', 'gre', 'hre', 'jre', 'kre', 'lre', 'mre', 'nre', 'pre', 'qre', 'rre', 'sre', 'tre', 'vre', 'wre', 'xre', 'zre', 'ire']


#CREATION DE LA MATRICE DES PROBABILITES DE TRANSITION DE LETTRES

 
#initialisation de la matrice des probabilités de transition à 0
mat_2 = [[[[0 for p in range(nb_lettre)] for k in range(lg_max)] for i in range(nb_lettre)]for j in range(nb_lettre)]

#comptage des occurences d'une lettre dans un mot en fonction 
#de sa position dans le mot et des deux lettres précédentes
for mot in lmot:
    if  len(mot) == 0:
        continue
    if '-' in mot: #pour les mots composés : on les considèrent comme deux mots séparés
        t_ = mot.index('-')
        mot1 = mot[:t_]
        n = len(mot1)
        mot2 = mot[t_+1:]
        if mot1 not in dmot:
            lmot.append(mot1)
        if mot2 not in dmot:
            lmot.append(mot2)
        mat_2[-1][-1][n][1] += 1 #probabilité d'être un mot composé dont le premier est de longueur n
    else:
        n = len(mot)
        mat_2[-1][-1][n][0] += 1 #probabilité d'être un mot simple de longueur n
        mat_2[-1][-1][0][id(mot[0])] += 1 #proba de la première lettre
        if n == 1:
            mat_2[-1][id(mot[0])][0][-1] += 1 #proba d'un mot d'une lettre
        if n >= 2:
            mat_2[-1][id(mot[0])][0][id(mot[1])] += 1 #proba de la deuxième lettre
            for i in range(1, n-1):
                mat_2[id(mot[i-1])][id(mot[i])][i][id(mot[i+1])] += 1 #proba de la lettre suivant la i-eme lettr
            mat_2[id(mot[n-2])][id(mot[n-1])][n-1][-1] += 1    #proba d'être la dernière lettre

#normalisation pour obtenir des probabilités
for i in range(nb_lettre):
    for j in range(nb_lettre):
        for k in range(lg_max):
            s = 0
            for p in range(nb_lettre):
                s += mat_2[i][j][k][p]
            if s != 0:
                for p in range(nb_lettre):
                    mat_2[i][j][k][p] /= s
 


# CREATION DES MOTS : le symbole '{' est utilisé pour symoboliser la fin d'un mot

#fonction qui associe à une suite de 0, 1 
def next_l(*l_1, pos = 0): 
    global liste_lettres   #ou 2 lettres la lettre suivant en fonction des probabilités calculées précedemment
    if len(l_1) == 0: #donne la première lettre
        return (random.choices(liste_lettres, weights = mat_2[-1][-1][pos]))[0]
    if len(l_1) == 1: #donne la deuxième lettre
        return (random.choices(liste_lettres, weights = mat_2[-1][id(l_1[0])][pos]))[0]
    if len(l_1) == 2:
        try: 
            lettre = (random.choices(liste_lettres, weights = mat_2[id(l_1[0])][id(l_1[1])][pos]))[0]
            return lettre
        except:
            return '{' #si toutes les probabilités sont nulles pour les lettres et la position considérée 
                        #on empêche l'erreur et on considère que le mot doit s'arrêter en retournant '{'
        

#fonction créant un pseudo-mot
def create_word(choix_debut = None):
    lettre1 = next_l()
    while lettre1 == '{': #pour éviter de créer un mot vide
        lettre1 = next_l()
    if choix_debut == 'c': #si l'on veut créer un mot qui commence avec une consonne
        while lettre1 not in consonnes:
            lettre1 = next_l()
    if choix_debut == 'v': #si l'on veut créer un mot qui commence avec une voyelle
        while lettre1 not in voyelles:
            lettre1 = next_l()
    lettre2 = next_l(lettre1)
    if lettre2 == '{': #création d'un mot d'une lettre
        return lettre1
    n = 2
    mot = lettre1 + lettre2
    while lettre2 != '{': #création d'un mot de n lettres
        lettre = next_l(lettre1, lettre2, pos = n-1)
        mot += lettre
        lettre1, lettre2 = lettre2, lettre
        n += 1
    compose_int = random.choices([False, True], weights = [mat_2[-1][-1][n - 1][0], mat_2[-1][-1][n - 1][1]]) #proba de creer un mot compose
    if n <= 26: 
        if compose_int[0]:
            return mot[:-1] + '-' + create_word()
    if mot[:-1] in dmot: #création de mots qui n'existent pas uniquement
        return create_word()
    return mot[:-1]

def create_words(n, url): #fonction creéant une liste de n pseudo-mot dans un fichier texte
    nom = url + '.txt'
    charabia = open(nom, 'w')
    for i in range(n):
        charabia.writelines(create_word())
        charabia.writelines('\n')
    charabia.close()

def create_verbs(n): #fonction qui créer des pseudo-verbe à l'infinitif
    charabia = open('verbs_charabia.txt', 'w')
    for i in range(n):
        mot = create_word()
        while mot[-2:] not in ['er', 'ir'] and mot[-3:] not in liste_term_troisieme_groupe:
            mot = create_word()
        charabia.writelines(mot)
        charabia.writelines('\n')
    charabia.close()



#create_words(10000, 'charabia')