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


def charge(fichier_texte, corpus):

    """
    Ouvre un livre en .txt, convertit son contenu en unicode utilisable et le nettoie.
    """

    with codecs.open(os.path.join(corpus,fichier_texte), "r", "utf-8") as file:
        texte = ''.join(unicodedata.normalize('NFC', line) for line in file.readlines())

    remplacements = {'\u202f':' ','\u200b':'','\u2002':' ', '\u2009':' ', '\xad':'','®':'', '‘':"'", 'ý':'y', '©':'', 'ÿ':'y', '⁂':'', '™':'', '“':'"', '»':'"', '  ':' ',"  ":" ", '«': '"', 
    '\t':'', '\n':' ', '\r':' ', '‑':'-', '–':'-', '—':'-', '―':'-', '−':'-', '’':'"', '”':'"', '„':'"', '•':'-'  }
    texte = multi_remplace(texte, remplacements)

    return texte


def gram(mot, nltk_g, lexicon, grams_equivalence, ponctuation, stops, noms_propres, precedents, proba, mots_vais):

    """
    reçoit un mot et renvoit son ou ses fonctions grammaticales
    renvoit 0 quand le mot n'est pas identifiable
    """

    if mot in ponctuation : return mot

    gm_gr_nb_iv = list(lexicon.get(mot.lower(),{}).keys())
    n_gr = len(gm_gr_nb_iv)

    if n_gr != 1:

        # le mot n'est pas présent dans lexicon
        if n_gr == 0 : 
            if mot in noms_propres or (mot.lower() != mot and (precedents or [None])[-1] not in stops):
                # le mot est déjà répertorié comme nom propre, ou contient une majuscule et n'est pas précédé d'un stop.
                noms_propres |= {mot}
                return 'NPR'
            digits = [c.isdigit()  for c in mot]
            if any(digits): 
                if all(digits): return 'ADJ:num'
                else:
                    if 'e' in mot[-3:]: return 'ADJ'
                    if mot[-1] == '°': return 'DEG'
            return 0

        # ambiguïté syntaxique, plusieurs gram possibles
        else:
            equi = grams_equivalence[nltk_g]
            intersection = [g for g in gm_gr_nb_iv if g[:3] in equi]
            if len(intersection) == 1:
                return intersection[0]

        return 0

    # une fonction grammaticale unique a été trouvée dans lexicon
    else : return gm_gr_nb_iv[0]


def probalimente(proba_table,precedents,g):

    """
    fonction qui remplit la table de probas du décompte des occurences
    """
    if precedents not in proba_table: proba_table[precedents] = {g : 1}
    else : proba_table[precedents][g] = proba_table[precedents].get(g, 0) +1 # fait en une ligne les deux suivantes
        # if g not in proba_table[precedents]: proba_table[precedents][g] = 1
        # else : proba_table[precedents][g] += 1


def analyse(prof_max):

    """
    Fonction principale, qui analyse tous les textes, à toutes les profondeurs jusqu'à prof_max
    et qui crée le fichier pkl de tables de probas pour chaque prof
    """

    local_path = os.path.dirname(__file__)

    # NLKTools
    jar = local_path + '/NLTK Tools/stanford-postagger-full-2020-11-17/stanford-postagger.jar'
    model = local_path + '/NLTK Tools/stanford-postagger-full-2020-11-17/models/french-ud.tagger'
    os.environ['JAVAHOME'] = 'C:/Program Files (x86)/Common Files/Oracle/Java/javapath'
    pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8' )

    # collection de Goncourts :
    corpus = os.path.dirname(__file__)+"/Data/Collection Prix Goncourt/txt"

    # lexicon :
    with open(local_path + '/Data/Lexicon_simplifié.pkl', "rb") as file:
        lexicon = pickle.load(file)
    
    ponctuation = {')', ':', '=','+','!','?',';','-','…','(','}',"'",',','{',']','"','.','['}
    stops = {':','!','?','-','…','(',"'",'"','.','['} # peuvent précéder les majuscules
    remplacements_ponct = {p : f' {p} ' for p in ponctuation}
    grams_equivalence = {
    "ADJ":{"ADJ"},
    "ADP":{"PRE"},
    "ADV":{"ADV"},
    "AUX":{"AUX"},
    "CCONJ":{"CON"},
    "DET":{"ART"},
    "INTJ":{"ONO"},
    "NOUN":{"NOM"},
    "NUM":{"ADJ:num","ADJ"},
    "PART":set(),
    "PRON":{"PRO"},
    "PROPN":{"NPR"},
    "PUNCT":set(),
    "SCONJ":{"CON"},
    "SYM":{"NOM"},
    "VERB":{"VER"},
    "X":set(),

    }

    noms_propres = set()
    mots_vais = set()

    ct_mots = [0]*prof_max
    ct_proba = [0]*prof_max
    probas = [{} for i in range(prof_max)]

    for filename in os.listdir(corpus):

        print(filename)
        # print("■", end='')
        texte = charge(filename, corpus)
        texte = multi_remplace(texte, remplacements_ponct)

        texte = texte.split()
        texte = pos_tagger.tag(texte)

        ct = 1 # compteur permettant de savoir si fifo est assez rempli pour produire une proba de profondeur prof
        fifo = deque(["."]) # Optimisation possible : affecter des entiers aux fonctions grammaticales 

        for prof in range(1,prof_max+1):

            print(prof,end = ' ')

            proba = probas[prof-1]

            for mot,nltk_g in texte:

                ct_mots[prof-1] += 1

                g = gram(mot, nltk_g, lexicon, grams_equivalence, ponctuation, stops, noms_propres, fifo, proba, mots_vais)

                if g == 0: # le mot n'a pas été trouvé dans lexicon
                # le mot est indéfini, on n'enregistre pas la suite de fonctions grammaticales, 
                # on saute au i suivant en vidant le fifo et remettant le compteur ct à 0

                    mots_vais |= {mot}
                    ct = 0
                    fifo = deque()
                    continue

                # le fifo ne contient pas encore assez de précédents
                if ct < prof:
                    fifo.append(g)
                    ct += 1
                    continue

                # Ajout proba de fifo et g dans la table
                tfifo = tuple(fifo)
                probalimente(proba,tfifo,g)
                ct_proba[prof-1] += 1
                fifo.append(g)
                fifo.popleft()
            
            print(ct_proba[prof-1]/ct_mots[prof-1])
        print()
    print()


    for prof in range(prof_max):

        # pickle dump de la table de proba de profondeur prof
        name = f"Syntaxe_proba_profondeur_{prof+1}.pkl"
        with open(local_path + f'/Transitions Tables/{name}', 'wb') as f:
            pickle.dump(probas[prof], f)
    
    # produire un fichier des mots rejettés par gram pour voir les failles
    with open(local_path + '/Data/mots_vais.txt', 'w') as f:
        f.write('\n'.join(sorted(mots_vais)))
    # produire un fichier des mots tagués commenoms propres
    with open(local_path + '/Data/noms_propres.txt', 'w') as f:
        f.write('\n'.join(sorted(noms_propres)))
    

prof_max = 11
analyse(prof_max)

# autour de 2000 secondes
