import codecs, unicodedata, random, re, pickle, os

#traitement de la liste de mot en liste python
remplacements = {'\x8a': '', '\u202f':' ','\u200b':'','\u2002':' ', '\u2009':' ', '\xad':'','®':'', '‘':"'", 'ý':'y', '©':'', 'ÿ':'y', '⁂':'', '™':'', '“':'"', '»':'"', '  ':' ',"  ":" ", '«': '"', 
    '\t':'', '\n':' ', '\r':' ', '‑':'-', '–':'-', '—':'-', '―':'-', '−':'-', '’':'"', '”':'"', '„':'"', '•':'-'  }
def multi_remplace(texte, remplacements):
    regex = re.compile('|'.join(map(re.escape, remplacements)))
    return regex.sub(lambda match: remplacements[match.group(0)], texte) 

local_path = os.path.dirname(__file__)

#fonction qui renvoie la liste de toutes les classes grammaticales qui nous serviront à créer des pseudos mots
def gram_a_charabie():
    gram_non_charabiées = {
    'DET','PRO','NPR','AUX_ind:pre:3s','VER_m_par:pas','VER_sub:imp:2s','VER_sub:pre:2p','VER_sub:pre:1p','CON','AUX_ind:pre:1s','AUX_sub:pre:1s','AUX_sub:pre:3p','AUX_sub:pre:2s','VER_sub:imp:1p','VER_ind:pas:2p','AUX_sub:pre:3s','AUX_ind:pre:2s','ART:def_m_s','ADJ:ind_m_s','PRO:ind_m_s','ADJ:ind_f_s','PRO:ind_f_s','ADJ:ind_f_p','ADJ:ind_m_p','PRO:int','PRO:rel_m_s','AUX_ind:fut:3s','AUX_inf','AUX_ind:fut:1s','AUX_cnd:pre:3p','AUX_cnd:pre:2s','AUX_cnd:pre:3s','AUX_ind:fut:2s','AUX_ind:fut:2p','AUX_cnd:pre:2p','AUX_cnd:pre:1p','AUX_ind:fut:1p','AUX_ind:fut:3p','PRO:ind_s','PRO:ind_p','PRO:ind_m_p','ART:def_p','PRO:rel_f_p','PRO:rel_m_p','AUX_ind:imp:3p','AUX_ind:imp:2s','AUX_ind:imp:3s','AUX_ind:pre:2p','AUX_ind:imp:2p','AUX_ind:imp:1p','AUX_ind:pre:1p','AUX_par:pre','AUX_sub:pre:2p','AUX_sub:pre:1p 2','PRO:dem','NOM','ADJ:dem_m_s','PRO:dem_m_s','PRO:dem_s','PRO:dem_f_s','PRO:dem_f_p','PRO:ind','PRO:ind_f_p','ADJ:dem_p','ADJ:dem_f_s','PRO:dem_m_p','ADJ:ind_s','PRO:per_s','VER_p_par:pas','ADJ:ind_p','ART:def_f_s','ART:ind_p','VER_sub:imp:2p','PRO:rel','PRO:per_f_s','PRO:per_f_p','PRO:per','AUX_m_s_par:pas','AUX_f_s_par:pas','AUX_f_p_par:pas','AUX_ind:pas:3p','AUX_m_p_par:pas','AUX_sub:imp:1s','AUX_sub:imp:3p','AUX_sub:imp:2s','AUX_sub:imp:2p','AUX_sub:imp:1p','AUX_ind:pas:3s','PRO:per_m_p','AUX_ind:pas:1p','AUX_sub:imp:3s','ADJ:ind','VER_imp:pre:3s','AUX_ind:pas:2s','AUX_ind:pas:2p','PRO:per_m_s','ADJ_f','ADJ:num_s','ART:def_s','PRO:ind_f','PRO:rel_f_s','PRO:per_p','PRO:pos_s','ADJ:pos','PRO:pos_p','ADJ:pos_m_s','PRO:pos_m_s','ADJ:pos_f_s','PRO:pos_f_s','ADJ:pos_f_p','PRO:pos_m_p','ADJ:pos_m_p','ADJ:pos_p','ADJ:pos_s','AUX_ind:pre:3p','ART:ind_m_s','ADJ:int_m_s','ADJ:int_f_s','ADJ:int_f_p','ADJ:int_m_p','PRO:rel_s','PRO:pos_f_p','ART:ind_f_s',
    }
    gram = ['ADJ', 'ADJ:dem_f_s', 'ADJ:dem_m_s', 'ADJ:dem_p', 'ADJ:ind', 'ADJ:ind_f_p', 'ADJ:ind_f_s', 'ADJ:ind_m_p', 'ADJ:ind_m_s', 'ADJ:ind_p', 'ADJ:ind_s', 'ADJ:int_f_p', 'ADJ:int_f_s', 'ADJ:int_m_p', 'ADJ:int_m_s', 'ADJ:num', 'ADJ:num_s', 'ADJ:pos', 'ADJ:pos_f_p', 'ADJ:pos_f_s', 'ADJ:pos_m_p', 'ADJ:pos_m_s', 'ADJ:pos_p', 'ADJ:pos_s', 'ADJ_f', 'ADJ_f_p', 'ADJ_f_s', 'ADJ_m', 'ADJ_m_p', 'ADJ_m_s', 'ADJ_p', 'ADJ_s', 'ADV', 'ART:def_f_s', 'ART:def_m_s', 'ART:def_p', 'ART:def_s', 'ART:ind_f_s', 'ART:ind_m_s', 'ART:ind_p', 'AUX_cnd:pre:1p', 'AUX_cnd:pre:2p', 'AUX_cnd:pre:2s', 'AUX_cnd:pre:3p', 'AUX_cnd:pre:3s', 'AUX_f_p_par:pas', 'AUX_f_s_par:pas', 'AUX_ind:fut:1p', 'AUX_ind:fut:1s', 'AUX_ind:fut:2p', 'AUX_ind:fut:2s', 'AUX_ind:fut:3p', 'AUX_ind:fut:3s', 'AUX_ind:imp:1p', 'AUX_ind:imp:2p', 'AUX_ind:imp:2s', 'AUX_ind:imp:3p', 'AUX_ind:imp:3s', 'AUX_ind:pas:1p', 'AUX_ind:pas:2p', 'AUX_ind:pas:2s', 'AUX_ind:pas:3p', 'AUX_ind:pas:3s', 'AUX_ind:pre:1p', 'AUX_ind:pre:1s', 'AUX_ind:pre:2p', 'AUX_ind:pre:2s', 'AUX_ind:pre:3p', 'AUX_ind:pre:3s', 'AUX_inf', 'AUX_m_p_par:pas', 'AUX_m_s_par:pas', 'AUX_par:pre', 'AUX_sub:imp:1p', 'AUX_sub:imp:1s', 'AUX_sub:imp:2p', 'AUX_sub:imp:2s', 'AUX_sub:imp:3p', 'AUX_sub:imp:3s', 'AUX_sub:pre:1p', 'AUX_sub:pre:1s', 'AUX_sub:pre:2p', 'AUX_sub:pre:2s', 'AUX_sub:pre:3p', 'AUX_sub:pre:3s', 'CON', 'NOM', 'NOM_f', 'NOM_f_p', 'NOM_f_s', 'NOM_m', 'NOM_m_p', 'NOM_m_s', 'NOM_p', 'NOM_s', 'NUM', 'ONO', 'ORD', 'PRE', 'PRO:dem', 'PRO:dem_f_p', 'PRO:dem_f_s', 'PRO:dem_m_p', 'PRO:dem_m_s', 'PRO:dem_s', 'PRO:ind', 'PRO:ind_f', 'PRO:ind_f_p', 'PRO:ind_f_s', 'PRO:ind_m_p', 'PRO:ind_m_s', 'PRO:ind_p', 'PRO:ind_s', 'PRO:int', 'PRO:per', 'PRO:per_f_p', 'PRO:per_f_s', 'PRO:per_m_p', 'PRO:per_m_s', 'PRO:per_p', 'PRO:per_s', 'PRO:pos_f_p', 'PRO:pos_f_s', 'PRO:pos_m_p', 'PRO:pos_m_s', 'PRO:pos_p', 'PRO:pos_s', 'PRO:rel', 'PRO:rel_f_p', 'PRO:rel_f_s', 'PRO:rel_m_p', 'PRO:rel_m_s', 'PRO:rel_s', 'VER_cnd:pre:1p', 'VER_cnd:pre:1s', 'VER_cnd:pre:2p', 'VER_cnd:pre:2s', 'VER_cnd:pre:3p', 'VER_cnd:pre:3s', 'VER_f_p_par:pas', 'VER_f_s_par:pas', 'VER_imp:pre:1p', 'VER_imp:pre:2p', 'VER_imp:pre:2s', 'VER_imp:pre:3s', 'VER_ind:fut:1p', 'VER_ind:fut:1s', 'VER_ind:fut:2p', 'VER_ind:fut:2s', 'VER_ind:fut:3p', 'VER_ind:fut:3s', 'VER_ind:imp:1p', 'VER_ind:imp:1s', 'VER_ind:imp:2p', 'VER_ind:imp:2s', 'VER_ind:imp:3p', 'VER_ind:imp:3s', 'VER_ind:pas:1p', 'VER_ind:pas:1s', 'VER_ind:pas:2p', 'VER_ind:pas:2s', 'VER_ind:pas:3p', 'VER_ind:pas:3s', 'VER_ind:pre:1p', 'VER_ind:pre:1s', 'VER_ind:pre:2p', 'VER_ind:pre:2s', 'VER_ind:pre:3p', 'VER_ind:pre:3s', 'VER_inf', 'VER_m_p_par:pas', 'VER_m_par:pas', 'VER_m_s_par:pas', 'VER_p_par:pas', 'VER_par:pre', 'VER_sub:imp:1p', 'VER_sub:imp:1s', 'VER_sub:imp:2p', 'VER_sub:imp:2s', 'VER_sub:imp:3p', 'VER_sub:imp:3s', 'VER_sub:pre:1p', 'VER_sub:pre:1s', 'VER_sub:pre:2p', 'VER_sub:pre:2s', 'VER_sub:pre:3p', 'VER_sub:pre:3s']
    gram = set(gram)
    gram_non_charabiées = set(gram_non_charabiées)
    return  list(gram - gram_non_charabiées)


def from_text_to_list(name, remplacements): #passer d'un fichier texte à une liste de mots
    with codecs.open(name, "r", "utf-8") as file:
        texte = ''.join(unicodedata.normalize('NFC', line) for line in file.readlines()) 
        texte = multi_remplace(texte, remplacements)
    return texte.split()

def lower(liste): #enlever les majuscules
    for i in range(len(liste)):
        liste[i] = liste[i].lower()
    
'''
fonction qui renvoie l'ensemble de tous le mots différents d'une liste, 
la liste de "lettres" ou caractères contenus différents dans une liste de mot qu'on appellera l'alphabet,
la longueur maximale des mots de la liste, 
et le nombre de 'lettres' (caractères) différentes contenues dans la liste
'''
def variables_utiles_liste(lmot):
    alphabet = set()
    dico = set()
    lg_max = 0
    for mot in lmot:
        if len(mot) > lg_max:
            lg_max = len(mot) #pour trouver la taille du mot le plus long
        dico.add(mot)
        for l in mot:
            alphabet.add(l)
    alphabet = list(alphabet)
    if '-' in alphabet:
        alphabet.remove('-') 
    alphabet.append('{') #ajout d'un marqueur de fin de mot
    nb_lettre = len(alphabet)
    return dico, alphabet, nb_lettre, lg_max + 1


#fonction qui renvoie la liste des consonnes et des voyelles dans une liste de lettres données
def cons_voy(alphabet):
    consonnes = []
    voyelles = []
    consonnes_max = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v',  'w', 'x', 'z',  'ç']
    voyelles_max = ['a', 'e', 'i', 'o', 'u', 'y', 'é', 'è', 'ê', 'à', 'ù', 'â', 'û', 'ô', 'ä', 'ï', 'ë', 'ü', 'ö', 'î']
    for l in alphabet:
        if l in consonnes_max:
            consonnes.append(l)
        if l in voyelles_max:
            voyelles.append(l)
    return consonnes, voyelles


#CREATION DE LA MATRICE DES PROBABILITES DE TRANSITION DE LETTRES

def create_mat(lmot, dico, alphabet, nb_lettre, lg_max, name = None): #elle sauvegarde cette matrice dans un fichier pickle si demandé

    #initialisation de la matrice des probabilités de transition à 0
    mat = [[[[0 for p in range(nb_lettre)] for k in range(lg_max)] for i in range(nb_lettre)]for j in range(nb_lettre)]
    
    #comptage des occurences d'une lettre dans un mot en fonction de sa position dans le mot et des deux lettres précédentes
    for mot in lmot:
        if  len(mot) == 0:
            continue
        if '-' in mot: #pour les mots composés : on les considère comme deux mots séparés
            t_ = mot.index('-')
            mot1 = mot[:t_]
            n = len(mot1)
            mot2 = mot[t_+1:]
            if mot1 not in dico:
                lmot.append(mot1)
            if mot2 not in dico:
                lmot.append(mot2)
            mat[-1][-1][n][1] += 1 #probabilité d'être un mot composé dont le premier est de longueur n
        else:
            n = len(mot)
            mat[-1][-1][n][0] += 1 #probabilité d'être un mot simple de longueur n
            mat[-1][-1][0][alphabet.index(mot[0])] += 1 #proba de la première lettre
            if n == 1:
                mat[-1][alphabet.index(mot[0])][0][-1] += 1 #proba d'un mot d'une lettre
            if n >= 2:
                mat[-1][alphabet.index(mot[0])][0][alphabet.index(mot[1])] += 1 #proba de la deuxième lettre
                for i in range(1, n-1):
                    mat[alphabet.index(mot[i-1])][alphabet.index(mot[i])][i][alphabet.index(mot[i+1])] += 1 #proba de la lettre suivant la i-eme lettr
                mat[alphabet.index(mot[n-2])][alphabet.index(mot[n-1])][n-1][-1] += 1    #proba d'être la dernière lettre

    #normalisation pour obtenir des probabilités
    for i in range(nb_lettre):
        for j in range(nb_lettre):
            for k in range(lg_max):
                s = 0
                for p in range(nb_lettre):
                    s += mat[i][j][k][p]
                if s != 0:
                    for p in range(nb_lettre):
                        mat[i][j][k][p] /= s

    if name is not None: #si demandé, elle conserve la matrice dans un fichier pickle ainsi que les variables importantes (car inutilisable sinon)
        with open(local_path + f'/../Data/Probas/Probas_inv_{name}.pkl', 'wb') as f:
            pickle.dump(mat, f)
        with open(local_path + f'/../Data/Probas/Variables_{name}.pkl', 'wb') as f:
            pickle.dump([dico, alphabet, nb_lettre, lg_max], f)
    return mat
 

# CREATION DES MOTS : le symbole '{' est utilisé pour symoboliser la fin d'un mot

def next_l(mat, alphabet, *l_1, pos = 0):
#fonction qui associe à une suite de 0, 1 ou 2 lettres la lettre suivant en fonction des probabilités calculées précedemment
    if len(l_1) == 0: #donne la première lettre
        return (random.choices(alphabet, weights = mat[-1][-1][pos]))[0]
    if len(l_1) == 1: #donne la deuxième lettre
        try:
            return (random.choices(alphabet, weights = mat[-1][alphabet.index(l_1[0])][pos]))[0]
        except:
            return '{'
    if len(l_1) == 2:
        try: 
            lettre = (random.choices(alphabet, weights = mat[alphabet.index(l_1[0])][alphabet.index(l_1[1])][pos]))[0]
            return lettre
        except:
            return '{' #si toutes les probabilités sont nulles pour les lettres et la position considérée 
                        #on empêche l'erreur et on considère que le mot doit s'arrêter en retournant '{'
        
#fonction créant un pseudo-mot
def create_word(mat, dico, alphabet, consonnes, voyelles,  choix_debut = None, starter = '', cpt = 0):
    if len(starter) < 2:
        mot = ''
        if len(starter) == 0:
            lettre1 = next_l(mat, alphabet)
            while lettre1 == '{': #pour éviter de créer un mot vide
                lettre1 = next_l(mat, alphabet)
            if choix_debut == 'c': #si l'on veut créer un mot qui commence avec une consonne
                while lettre1 not in consonnes:
                    lettre1 = next_l(mat, alphabet)
            if choix_debut == 'v': #si l'on veut créer un mot qui commence avec une voyelle
                while lettre1 not in voyelles:
                    lettre1 = next_l(mat, alphabet)
        if len(starter) == 1:
            lettre1 = starter
        lettre2 = next_l(mat, alphabet, lettre1)
        if lettre2 == '{' and len(starter) == 0: #création d'un mot d'une lettre
            return lettre1
    if len(starter) >= 2:
        lettre1 = starter[-2]
        lettre2 = starter[-1]
        mot = starter[:-2]
    mot += lettre1
    mot += lettre2
    n = len(mot)
    mot = lettre1 + lettre2
    while lettre2 != '{': #création d'un mot de n lettres
        lettre = next_l(mat, alphabet, lettre1, lettre2, pos = n-1)
        mot += lettre
        lettre1, lettre2 = lettre2, lettre
        n += 1
    try:
        compose = random.choices([False, True], weights = [mat[-1][-1][n - 1][0], mat[-1][-1][n - 1][1]]) #proba de creer un mot compose
    except:
        compose = False #si il n'y a pas de mots composés dans le corpus de départ, pour éviter l'erreur
    if n <= 26: 
        if compose[0]:
            return mot[:-1] + '-' + create_word(mat, dico, alphabet, consonnes, voyelles)
    if mot[:-1] in dico and cpt < 3: #création de mots qui n'existent pas uniquement, si il ne peut que créer un mot qui existe à cause d'un corpus de mot, trop restreint, il finit par renvoyer un mot quelqu'il soit
        cpt += 1
        return create_word(mat, dico, alphabet, consonnes, voyelles,  choix_debut = choix_debut, starter = starter, cpt = cpt)
    return mot[:-1]


def create_words(mat, dico, alphabet, consonnes, voyelles, n, url): #fonction creéant une liste de n pseudo-mot dans un fichier texte
    nom = url + '.txt'
    charabia = open(nom, 'w')
    for i in range(n):
        charabia.writelines(create_word(mat,dico, alphabet, consonnes, voyelles))
        charabia.writelines('\n')
    charabia.close()

# création des fichier pickle contenant la matrice de transition pour chaque classe grammaticale
# il crée aussi les variables importantes pour chaque nature
with open(local_path + '/../Data/Lexicon_inverse.pkl', "rb") as file:
	lexicon_inv = pickle.load(file)

def create_mat_charabiation():
    gram_liste = gram_a_charabie()
    with open(local_path + f'/../Data/Probas/gram_liste.pkl', 'wb') as f:
            pickle.dump(gram_liste, f)
    for i in range(len(gram_liste)):
        liste_mot = list(lexicon_inv[gram_liste[i]].keys())
        Variable = variables_utiles_liste(liste_mot)
        create_mat(liste_mot, Variable[0], Variable[1], Variable[2], Variable[3], name = str(i))
        

        