
"""
Prend un extrait de Goncourt, et remplace quelques mots de cet extrait par du charabia
Mais du charabia précis : créé à partir de mots de la même nature que le mot remplacé
"""

import codecs, unicodedata, os, pickle, random, re
from nltk.tag import StanfordPOSTagger
from Generateur_matrice_par_nature import create_word

local_path = os.path.dirname(__file__)

# NLKTools
jar = local_path + '/../Tools/NLTK_Tools/stanford-postagger-full-2020-11-17/stanford-postagger.jar'
model = local_path + '/../Tools/NLTK_Tools/stanford-postagger-full-2020-11-17/models/french-ud.tagger'

# Là il faut indiquer l'adresse de Java dans l'ordi
# os.environ['JAVAHOME'] = 'C:/Program Files (x86)/Common Files/Oracle/Java/javapath'
os.environ['JAVAHOME'] = 'C:/Program Files/Java/jre1.8.0_351/'

pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8' )

#liste de toutes les natures à charabier
with open(local_path + '/../Data/Probas/gram_liste.pkl', 'rb') as file:
    gram_pour_charabie = pickle.load(file)

def multi_remplace(texte, remplacements):

    """
    outil regex de remplacement de plusieurs str en une passe, 
    utilisant un dictionnaire de remplacements
    """
    regex = re.compile('|'.join(map(re.escape, remplacements)))
    return regex.sub(lambda match: remplacements[match.group(0)], texte)

  
def trouveur_extrait(année_voulue, ponctuation, local_path, gros_texte, n_mots = None, goncourt = None):
    """
    renvoie un extrait de n phrases du livre dont l'année est la plus proche de l'année voulue, sous forme de liste  
    """
    stops = {'.','?','!'}
    pas_lettres = {' ', '\n'} | ponctuation
    if gros_texte:
        if goncourt == 'g':
        # Ouvre Goncourt de l'année la plus proche de l'année demandée
            noms_livres = os.listdir(local_path+'/../Data/Collection_Prix_Goncourt/txt')
            années = [nom_livre[:4] for nom_livre in noms_livres]
            années_diff = []
            for i,année in enumerate(années) :
                années_diff += [(abs(année_voulue - int(année)), i)]
            titre_voulu = noms_livres[min(années_diff)[1]]
            
            with codecs.open(local_path+'/../Data/Collection_Prix_Goncourt/txt/'+titre_voulu, "r", "utf-8") as file:
                texte = ''.join(unicodedata.normalize('NFC', line) for line in file.readlines())
        else:
            texte = année_voulue
        # Nettoyage texte : pour homogénéiser les espaces et tirets moches
        remplacements = {'\u202f':' ','\u200b':'','\u2002':' ', '\u2009':' ', '\xad':'','‑':'-', '–':'-', '—':'-', '―':'-', '−':'-'}
        texte = multi_remplace(texte, remplacements)


        # Séparation n mots / espace et ponctuations (split maison)
        texte_splité = []
        mots_id = []
        mot = ''

        for i,car in enumerate(texte):
            if car in pas_lettres:
                if mot != '': # mot fini 
                    texte_splité += [mot]
                    mots_id += [len(texte_splité)-1]
                    mot = ''
                texte_splité += [car]
            else:
                mot += car

        # autoriser max deux sauts de lignes consécutifs
        sauts = 0
        for i,c in enumerate(texte_splité):
            if c in {"\n","\r"," "}:
                if c in {"\n","\r"}: sauts += 1
            else:
                sauts = 0
            if sauts > 3: texte_splité[i] = ''


        # Début extrait aléatoire
        fin_texte_sécurité = mots_id[len(mots_id) - n_mots - 500]
        i_début_extrait = random.randint(0, fin_texte_sécurité)

        # Je démarre au premier mot suivant le premier point rencontré
        for i in range(i_début_extrait,len(texte_splité)):
            e = texte_splité[i]
            if e in stops:
                while e in stops | {'\r', '\n', ' ',')'}: # on pourrait aussi vérifier que le prochain mot a une majuscule (mais pb jamais rencontré)
                    i += 1
                    e = texte_splité[i]
                break
        debut = i

        mots_id = [mi for mi in mots_id if mi >= debut]
        nième_mot = mots_id[n_mots]

        # Je cherche le premier point après le nième mot
        for j in range(nième_mot,len(texte_splité)):
            e = texte_splité[j]
            if e in stops:
                fin = j+1
                break

        extrait = texte_splité[debut:fin]
    else:
        # Séparation n mots / espace et ponctuations (split maison)
        texte_splité = []
        mot = ''
        texte = année_voulue

        for i,car in enumerate(texte):
            if car in pas_lettres:
                if mot != '': # mot fini 
                    texte_splité += [mot]
                    mot = ''
                texte_splité += [car]
            else:
                mot += car
        extrait = texte_splité
    return extrait


def grammatise(extrait, local_path):
    """
    renvoie une liste de listes [mot, gram] dont les mots sont ceux de l'extrait et gram leur nature grammaticale
    """
    # lexicon
    with open(local_path + '/../Data/Lexicon_simplifié.pkl', "rb") as file: 
        lexicon = pickle.load(file)
    # noms propres
    with open(local_path + '/../Data/noms_propres.txt', "r") as file: 
        noms_propres = set(file.readlines())
    grams_equivalence = {"ADJ":{"ADJ"},"ADP":{"PRE"},"ADV":{"ADV"},"AUX":{"AUX"},"CCONJ":{"CON"},"DET":{"ART"},"INTJ":{"ONO"},
    "NOUN":{"NOM"},"NUM":{"ADJ"},"PART":set(),"PRON":{"PRO"},"PROPN":{"NPR"},"PUNCT":set(),"SCONJ":{"CON"},"SYM":{"NOM"},
    "VERB":{"VER"},
    "X":set(),
    }

    nltk_extrait = ((m,g) for m,g in pos_tagger.tag(extrait) if g != 'PUNCT')

    i = 0
    for mot,nltk_g in nltk_extrait:
        while i < len(extrait):
            e = extrait[i]
            if e != mot: i += 1
            else:
                # on cherche la fonction gram du lexicon en filtrant avec nltk 
                lexi_g = list(lexicon.get(mot.lower(),{}).keys())
                n_gr = len(lexi_g)
                if n_gr != 1:
                    # le mot n'est pas présent dans lexicon
                    if n_gr == 0 : 
                        if mot in noms_propres: gram = 'NPR'
                        else:
                            digits = [c.isdigit() for c in mot]
                            if any(digits): 
                                if all(digits): gram = 'ADJ:num'
                                else:
                                    if 'e' in mot[-3:]: gram = 'ADJ' # Ordinal
                                    if mot[-1] == '°': gram = 'DEG'
                            else: gram = 0

                    # ambiguïté syntaxique, plusieurs gram possibles
                    else:
                        equi = grams_equivalence[nltk_g]
                        intersection = [g for g in lexi_g if g[:3] in equi]
                        gram = intersection[0] if len(intersection) == 1 else 0

                # une fonction grammaticale unique a été trouvée dans lexicon
                else : gram = lexi_g[0]
                extrait[i] = (mot,gram)
                i += 1
                break

    return [mg if isinstance(mg,tuple) else (mg,0) for mg in extrait]



'''
Fonction qui à un mot du texte le remplace par un pseudo_mot
'''

def charabieur_mot(mot, gram, dico_charabie): 
    ieme = False
    if gram == 'ORD': #pour les ordinaux, le lexicon est trop approximatif
        ieme = True
        gram = 'NUM'
    indice = gram_pour_charabie.index(gram)
    starter = ''
    maj = False
    grand = False
    consonnes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v',  'w', 'x', 'z',  'ç']
    voyelles= ['a', 'e', 'i', 'o', 'u', 'y', 'é', 'è', 'ê', 'à', 'ù', 'â', 'û', 'ô', 'ä', 'ï', 'ë', 'ü', 'ö', 'î']
    if mot[0].upper() == mot[0]: #pour conserver les majuscules
        maj = True
    if mot.upper() == mot:
        grand = True
        maj = False
    if mot[0].lower() in voyelles: #pour conserver le type (voyelle/consonne) de la première lettre
        choix_debut = 'v'
    else:
        if mot[0].lower() == 'h': # si le mot commence par h, le nouveau-mot également
            starter = 'h'
        choix_debut = 'c'
    name = str(indice)
    with open(local_path + f'/../Data/Probas/Probas_inv_{name}.pkl', "rb") as file_1: 
        mat = pickle.load(file_1)
    with open(local_path + f'/../Data/Probas/Variables_{name}.pkl', 'rb') as file_2:
            Variables = pickle.load(file_2)
    mot_new = create_word(mat, Variables[0], Variables[1], consonnes, voyelles,  choix_debut = choix_debut, starter=starter)
    while len(mot_new) < 4: #création de mot de longueur 4 minimum
        mot_new = create_word(mat, Variables[0], Variables[1], consonnes, voyelles,  choix_debut = choix_debut, starter=starter)
    if maj:
        mot_new = mot_new[0].upper() + mot_new[1:]
    if grand:
        mot_new = mot_new.upper()
    if gram != 'ADJ:num' and gram != 'NUM': #toujours charabier un même mot de la même façon sauf pour les nombres
        dico_charabie[mot] = mot_new
    if ieme: #pour les ordinaux, rajouter le suffixe ième de façon adéquate
        if mot_new[-1] == 'e':
            mot_new = mot_new[-1] + 'ième'
        elif mot_new[-1] == 'f':
            mot_new = mot_new[-1] + 'vième'
        elif mot_new[-1] == 'q':
            mot_new += 'uième'
        else:
            mot_new += 'ième'
    return mot_new


def charabieur(année_voulue, proba_charabia, gros_texte, n_mots = None, goncourt = None):
    """
    renvoie un extrait de goncourt de l'année voulue dont certains mots sont remplacés par du charabia
    """
    local_path = os.path.dirname(__file__)
    ponctuation = {')', ':', '=','+','!','?',';','-','…','(','}',"'",'’',',','{',']','"','.','['}
    # charge une seule fois le lexicon inversé et les probas qui ont été faites avec
    with open(local_path + '/../Data/Lexicon_inverse.pkl', "rb") as file: lexicon_inv = pickle.load(file)
    # Les probas créés par le code de Joz
    extrait = trouveur_extrait(année_voulue, ponctuation, local_path, gros_texte, n_mots= n_mots, goncourt = goncourt)

    extrait_gram = grammatise(extrait, local_path)

    gram_non_charabiées = {
    'DET','PRO','NPR','AUX_ind:pre:3s','VER_m_par:pas','VER_sub:imp:2s','VER_sub:pre:2p','VER_sub:pre:1p','CON','AUX_ind:pre:1s','AUX_sub:pre:1s','AUX_sub:pre:3p','AUX_sub:pre:2s','VER_sub:imp:1p','VER_ind:pas:2p','AUX_sub:pre:3s','AUX_ind:pre:2s','ART:def_m_s','ADJ:ind_m_s','PRO:ind_m_s','ADJ:ind_f_s','PRO:ind_f_s','ADJ:ind_f_p','ADJ:ind_m_p','PRO:int','PRO:rel_m_s','AUX_ind:fut:3s','AUX_inf','AUX_ind:fut:1s','AUX_cnd:pre:3p','AUX_cnd:pre:2s','AUX_cnd:pre:3s','AUX_ind:fut:2s','AUX_ind:fut:2p','AUX_cnd:pre:2p','AUX_cnd:pre:1p','AUX_ind:fut:1p','AUX_ind:fut:3p','PRO:ind_s','PRO:ind_p','PRO:ind_m_p','ART:def_p','PRO:rel_f_p','PRO:rel_m_p','AUX_ind:imp:3p','AUX_ind:imp:2s','AUX_ind:imp:3s','AUX_ind:pre:2p','AUX_ind:imp:2p','AUX_ind:imp:1p','AUX_ind:pre:1p','AUX_par:pre','AUX_sub:pre:2p','AUX_sub:pre:1p 2','PRO:dem','NOM','ADJ:dem_m_s','PRO:dem_m_s','PRO:dem_s','PRO:dem_f_s','PRO:dem_f_p','PRO:ind','PRO:ind_f_p','ADJ:dem_p','ADJ:dem_f_s','PRO:dem_m_p','ADJ:ind_s','PRO:per_s','VER_p_par:pas','ADJ:ind_p','ART:def_f_s','ART:ind_p','VER_sub:imp:2p','PRO:rel','PRO:per_f_s','PRO:per_f_p','PRO:per','AUX_m_s_par:pas','AUX_f_s_par:pas','AUX_f_p_par:pas','AUX_ind:pas:3p','AUX_m_p_par:pas','AUX_sub:imp:1s','AUX_sub:imp:3p','AUX_sub:imp:2s','AUX_sub:imp:2p','AUX_sub:imp:1p','AUX_ind:pas:3s','PRO:per_m_p','AUX_ind:pas:1p','AUX_sub:imp:3s','ADJ:ind','VER_imp:pre:3s','AUX_ind:pas:2s','AUX_ind:pas:2p','PRO:per_m_s','ADJ_f','ADJ:num_s','ART:def_s','PRO:ind_f','PRO:rel_f_s','PRO:per_p','PRO:pos_s','ADJ:pos','PRO:pos_p','ADJ:pos_m_s','PRO:pos_m_s','ADJ:pos_f_s','PRO:pos_f_s','ADJ:pos_f_p','PRO:pos_m_p','ADJ:pos_m_p','ADJ:pos_p','ADJ:pos_s','AUX_ind:pre:3p','ART:ind_m_s','ADJ:int_m_s','ADJ:int_f_s','ADJ:int_f_p','ADJ:int_m_p','PRO:rel_s','PRO:pos_f_p','ART:ind_f_s',
    } 

    dico_charabie = {}
    # Sélection des mots que l'on va charabier
    for i, (mot, gram) in enumerate(extrait_gram) :
        if len(mot)>4 and gram != 0 and gram not in gram_non_charabiées:
            if mot in dico_charabie.keys(): #un mot qui a été déjà remplacé est toujours remplacé de la même façon
                mot = dico_charabie[mot]
                extrait_gram[i] = (mot, gram)
            else:
                on_charabie = random.choices([0,1], weights=[1-proba_charabia, proba_charabia])[0]
                if on_charabie :
                    mot = charabieur_mot(mot, gram, dico_charabie)
                    extrait_gram[i] = (mot,gram)
        if gram == 0:
            continue
    extrait_charabié = ''.join([m for m,g in extrait_gram])

    print()
    print(extrait_charabié)

while True:
    while True:
        goncourt = input('Quel texte voulez-vous charabier ? Pour un Goncourt tapez : g, pour un fichier texte t, ou sinon n\'importe quoi : ')
        gros_texte = False
        if goncourt == 'g' or goncourt == 'G':
            gros_texte = True 
            année_voulue = input("Année du Goncourt à charabier (entre 1903 et 2022) : ")
            try :
                année_voulue = int(année_voulue)
                if 1903 <= année_voulue <= 2022: break
                else: print("Pas bien, akhor !")
            except:
                print("Nan nan nan ! Reko-mencer !")
        if goncourt == 't' or goncourt == 'T':
            gros_texte = True
            année_voulue = ''
            name_text = input('Entrez le nom du fichier à charabier (IL DOIT SE TROUVER DANS DATA) :')
            try:
                with codecs.open(local_path + f'/../Data/{name_text}.txt' , "r", "utf-8") as file:
                    année_voulue = ''.join(unicodedata.normalize('NFC', line) for line in file.readlines())
            except:
                print('Fichier non trouvé')
            break
        else:
            année_voulue = input('Saisissez le texte à charabier : ') 
            n_mots = None
            break

    while gros_texte:
        n_mots = input("Nombre de mots de l'extrait (max = 2000): ")
        try:
            n_mots = int(n_mots)
            if 0 < n_mots <= 2000: break
            else: print("Sinon, compte avec tes doigts")
        except: 
            print("Eh on a dit nombre") 

    proba_charabia = 0.6 # proba de charabia parmi les mots que l'on peut et veut charabier

    charabieur(année_voulue, proba_charabia, gros_texte, n_mots = n_mots, goncourt = goncourt)
    print()

"""
Ils passèrent le barioleur sur le pont de Malvaux. A travers les crisoldats en loques tombaient des arboursuiciers de soleil merdâtres.  
"""