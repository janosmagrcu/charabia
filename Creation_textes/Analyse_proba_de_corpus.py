import os, codecs, unicodedata, re, pickle
from collections import deque
from nltk.tag import StanfordPOSTagger


def multi_remplace(texte, remplacements):

    """
    outil regex de remplacement de plusieurs str en une passe, 
    utilisant un dictionnaire de remplacements
    """

    regex = re.compile('|'.join(map(re.escape, remplacements)))
    return regex.sub(lambda match: remplacements[match.group(0)], texte)


def probalimente(proba_table,precedents,g):

    """
    fonction qui remplit la table de probas du décompte des occurences
    """
    if precedents not in proba_table: proba_table[precedents] = {g : 1}
    else : proba_table[precedents][g] = proba_table[precedents].get(g, 0) +1

def split_maison(texte):

    # Séparation n mots / espace et ponctuations (split maison)
    texte_splité = []
    mot = ''

    for car in texte:
        # les mots composés (avec '-' entre deux lettres) sont gardés entiers    
        if car.isalpha() or (car =='-' and mot != ''): mot += car
        else:
            if mot != '': # mot fini 
                texte_splité += [mot]
                mot = ''
            texte_splité += [car]
    return texte_splité

def pos_tag(texte, avec_nltk, pos_tagger, lexicon, grams_equivalence, ponctuation, stops, noms_propres, mots_vais):

    espaces = ' \t'
    sauts = '\n\r'

    if avec_nltk:
        merge = []
        texte_nltk = iter(pos_tagger.tag(texte))
        nltk_e,nltk_g = next(texte_nltk)
        for e in texte:
            if e == nltk_e: 
                merge += [(nltk_e,nltk_g)]
                nltk_e,nltk_g = next(texte_nltk,('',''))
            else:
                merge += [(e,'')]

    else: merge = [(e,'') for e in texte]

    for i, (mot,gram) in enumerate(merge):

        if mot in ponctuation:
            # gestion du tiret '-'
            if mot == '-':
                j = i-1
                while j >= 0:
                    prec = merge[j][0]
                    if prec in espaces: j -= 1
                    elif prec in sauts:
                        gram = "DIA" # pour dialogue
                        break
                    else: 
                        gram = '-'
                        break
            # autres signes de ponctuation, le gram est le signe lui-même
            else: 
                gram = mot

        elif mot in {'ne','ni'}: gram = mot

        else:
            lexi_g = list(lexicon.get(mot.lower(),{}).keys())
            n_lexi_g = len(lexi_g)

            if n_lexi_g != 1:

                # le mot n'est pas présent dans lexicon
                if n_lexi_g == 0 :
                    if any(digits := [c.isdigit()  for c in mot]): 
                        # nombres en chiffres
                        if all(digits): gram = 'ADJ:num'
                        else:
                            if 'e' in mot[-3:]: gram = 'ORD'
                            elif mot[-1] == '°': gram = 'DEG'
                            else: gram = 'ADJ:num'
                    elif mot in noms_propres: 
                        # le mot est déjà répertorié comme nom propre
                        gram = 'NPR'
                    elif mot.lower() != mot or gram == 'PROPN':
                        # il y a (au moins) une majuscule
                        j = i-1
                        while j>=0:
                            prec = merge[j][0]
                            if prec in stops: 
                                gram = 'NPR' if gram == 'PROPN' else 0
                                break
                            elif prec.isalpha():
                                gram = 'NPR'
                                noms_propres |= {mot.lower()}
                                break
                            j -= 1
                    else: 
                        gram = 0

                # ambiguïté syntaxique, plusieurs gram possibles
                else:
                    if gram:
                        equi = grams_equivalence[gram]
                        intersection = [g for g in lexi_g if g[:3] in equi]
                        if len(intersection) == 1:
                            gram = intersection[0]
                        else: gram = 0
                    else: gram = 0

            # une fonction grammaticale unique a été trouvée dans lexicon
            else :
                gram = lexi_g[0]

        texte[i] = (mot, gram)

    return texte


def analyse(prof_max):

    """
    Fonction principale, qui analyse tous les textes, à toutes les profondeurs jusqu'à prof_max
    et qui crée le fichier pkl de tables de probas pour chaque prof
    """

    local_path = os.path.dirname(__file__)

    # NLKTools
    if avec_nltk:
        jar = local_path + '/../Tools/NLTK_Tools/stanford-postagger-full-2020-11-17/stanford-postagger.jar'
        model = local_path + '/../Tools/NLTK_Tools/stanford-postagger-full-2020-11-17/models/french-ud.tagger'
        os.environ['JAVAHOME'] = 'C:/Program Files (x86)/Common Files/Oracle/Java/javapath'
    pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8' ) if avec_nltk else ''

    # collection de Goncourts :
    corpus = os.path.dirname(__file__)+"/../Data/Collection_Prix_Goncourt/txt"

    # lexicon :
    with open(local_path + '/../Data/Lexicon_simplifié.pkl', "rb") as file:
        lexicon = pickle.load(file)
    
    ponctuation = '):=+!?;-…(},{]".['
    stops = ':!?-…(\'".[' # peuvent précéder les majuscules
    vides = "' \t\n\r"
    remplacements = {'\u202f':' ','\u200b':'','\u2002':' ', '\u2009':' ', '\xad':'', '‘':"'",
                    '⁂':'', '“':'"', '»':'"', '  ':' ',"  ":" ", '«': '"','‑':'-','–':'-',
                    '—':'-','―':'-','−':'-','’':"'",'”':'"','„':'"','•':'-','...':'…'}

    grams_equivalence = {"ADJ":{"ADJ"},"ADP":{"PRE"},"ADV":{"ADV"},"AUX":{"AUX"},"CCONJ":{"CON"},
    "DET":{"ART"},"INTJ":{"ONO"},"NOUN":{"NOM"},"NUM":{"ADJ:num","ADJ"},"PART":set(),"PRON":{"PRO"},
    "PROPN":{"NPR"},"PUNCT":set(),"SCONJ":{"CON"},"SYM":{"NOM"},"VERB":{"VER"},"X":set(),}

    for prof in range(prof_max):
        probas = {}
        # pickle dump de la table de proba vide de profondeur prof
        name = f"Proba_profondeur_{prof+1}.pkl"
        with open(local_path + f'/../Data/Probas/Creation_textes_{("","nltk_")[avec_nltk]}{name}', 'wb') as f:
            pickle.dump(probas, f)

    noms_propres = set()
    mots_vais = set()

    # compteurs permettant de connaître la proportion de mots produisant des probas
    ct_mots = [0]*prof_max
    ct_proba = [0]*prof_max

    for titre_livre in os.listdir(corpus):

        print(titre_livre)
        # print("■", end='')

        with codecs.open(os.path.join(corpus,titre_livre), "r", "utf-8") as file:
            texte = ''.join(unicodedata.normalize('NFC', line) for line in file.readlines())

        texte = multi_remplace(texte, remplacements)
        texte = split_maison(texte)
        texte = pos_tag(texte, avec_nltk, pos_tagger, lexicon, grams_equivalence, ponctuation, stops, noms_propres, mots_vais)

        ct = 1 # compteur permettant de savoir si fifo est assez rempli pour produire une proba de profondeur prof
        fifo = deque(["."]) # Optimisation possible : affecter des entiers aux fonctions grammaticales 

        for prof in range(1,prof_max+1):

            print(prof,end = ' ')

            # ouvrir la table proba de prodondeur prof
            name = f"Proba_profondeur_{prof}.pkl"
            with open(local_path + f'/../Data/Probas/Creation_textes_{("","nltk_")[avec_nltk]}{name}', 'rb') as f:
                probas = pickle.load(f)

            for mot,gram in texte:

                if mot in vides: continue

                ct_mots[prof-1] += 1

                if gram == 0: # le mot n'a pas été trouvé dans lexicon
                # le mot est indéfini, on n'enregistre pas la suite de fonctions grammaticales, 
                # on saute au i suivant en vidant le fifo et remettant le compteur ct à 0

                    mots_vais |= {mot}
                    ct = 0
                    fifo = deque()
                    continue

                # le fifo ne contient pas encore assez de précédents
                if ct < prof:
                    fifo.append(gram)
                    ct += 1
                    continue

                # Ajout proba de fifo : gram dans la table
                tfifo = tuple(fifo)
                probalimente(probas,tfifo,gram)
                ct_proba[prof-1] += 1
                fifo.append(gram)
                fifo.popleft()
            
            print(ct_proba[prof-1]/ct_mots[prof-1])

            with open(local_path + f'/../Data/Probas/Creation_textes_{("","nltk_")[avec_nltk]}{name}', 'wb') as f:
                pickle.dump(probas, f)

        print()
    print()
    
    # produire un fichier des mots rejettés par gram pour voir les failles
    with open(local_path + f'/../Data/mots_vais{("","nltk_")[avec_nltk]}.txt', 'w') as f:
        f.write('\n'.join(sorted(mots_vais)))
    # produire un fichier des mots tagués commenoms propres
    with open(local_path + f'/../Data/noms_propres{("","nltk_")[avec_nltk]}.txt', 'w') as f:
        f.write('\n'.join(sorted(noms_propres)))


prof_max = 15
avec_nltk = 0
analyse(prof_max)