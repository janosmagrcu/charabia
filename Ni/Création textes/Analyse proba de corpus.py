import os, codecs, unicodedata, re, pickle
from collections import deque

"""
Crée un dossieer Tables de transitions dans Data et créé les tables statistiques de profondeur 1 à prof_max sous forme de fichiers pickle dans ce dossier
Prend environ 7 minutes

"""
# collection de Goncourts :
corpus = os.path.dirname(__file__)+"/Data/Collection Prix Goncourt/txt"

def multi_remplace(texte, remplacements):
    """
    remplace les clés du dictionnaire remplacements par leurs valeurs dans texte
    """

    regex = re.compile('|'.join(map(re.escape, remplacements)))
    return regex.sub(lambda match: remplacements[match.group(0)], texte)


def charge(fichier_texte):
    """
    Ouvre un livre en .txt, convertit son contenu en unicode utilisable et le nettoie
    """

    with codecs.open(os.path.join(corpus,fichier_texte), "r", "utf-8") as file:
        texte = ''.join(unicodedata.normalize('NFC', line) for line in file.readlines())

    remplacements = {'\u202f':' ','\u200b':'','\u2002':' ', '\u2009':' ', '\xad':'','®':'', '‘':"'", 'ý':'y', '©':'', 'ÿ':'y', '⁂':'', '™':'', '“':'"', '»':'"', '  ':' ',"  ":" ", '«': '"', 
    '\t':'', '\n':' ', '\r':' ', '‑':'-', '–':'-', '—':'-', '―':'-', '−':'-', '’':'"', '”':'"', '„':'"', '•':'-'  }
    texte = multi_remplace(texte, remplacements)

    return texte


def gram(mot, lexicon, ponctuation, stops, noms_propres, passe, precedents, proba_p1):

    """
    reçoit un mot et renvoit sa ou ses fonctions grammaticales
    renvoit 0 quand le mot n'est pas identifiable dans lexicon
    """

    if mot in ponctuation : return mot

    gm_gr_nb_iv = lexicon.get(mot.lower(),[])
    n_gr = len(gm_gr_nb_iv)

    if n_gr != 1:

        if n_gr == 0 : # le mot n'est pas présent dans lexicon
            if mot in noms_propres or (mot.lower() != mot and (precedents or [None])[-1] not in stops):
                # le mot est déjà répertorié comme nom propre, ou contient une majuscule et n'est pas précédé d'un stop.
                noms_propres |= {mot}
                return 'NPR'
            if any(c.isdigit() for c in mot):
                return 'NUM'
            return 0

        # n_gr > 1, le mot peut avoir plusieurs fonctions grammaticales
        if passe: # on est dans la 2eme passe => on tient compte des probas déjà calculées en 1ere passe

            deja_vu = proba_p1.get(tuple(precedents),{})

            # La combinaison de fonctions gram précédentes a déjà donné lieu à un décompte
            intersection = [(n,g) for g,n in deja_vu.items() if g in gm_gr_nb_iv]

            # une fonction gramaticale du mot présent fait partie de déjà vu
            if intersection: return max(intersection)[1]

        return 0

    # une fonction grammaticale unique a été trouvée dans lexicon
    else : return gm_gr_nb_iv[0]


def probalimente(proba_table,precedents,g):
    """
    remplit la table de probas du décompte des occurences
    """
    if precedents not in proba_table: proba_table[precedents] = {g : 1}
    else : proba_table[precedents][g] = proba_table[precedents].get(g, 0) +1


def analyse(corpus, lexicon, prof, local_path):
    
    ponctuation = {')', ':', '=','+','!','?',';','-','…','(','}',"'",',','{',']','"','.','['}
    stops = {':','!','?','-','…','(',"'",'"','.','['} # peuvent précéder les majuscules
    remplacements_ponct = {p : f' {p} ' for p in ponctuation}
    noms_propres = set()

    proba_p1 = {}
    proba_p2 = {}
    
    for passe in range(2):
        # l'analyse se fait en deux passes, la première passe ne tient pas compte des 
        # occurences de mots qui ont plusieurs fonctions grammaticales possibles,
        # la deuxième passe les utilise pour renforcer la fonction la plus probable 
        # déjà calculée dans le cas des mêmes précédents
        proba = [proba_p1,proba_p2][passe]
        # chaque passe produit une table de proba différente, la deuxième sera plus complète

        mots_vais = set()

        ct_mots = 0
        ct_rejet = 0
        ct_proba = 0

        for filename in os.listdir(corpus):

                # print(filename)
                print("■", end='')
                texte = charge(filename)
                texte = multi_remplace(texte, remplacements_ponct)
                texte = texte.split()

                ct = 1
                fifo = deque(["."])

                for mot in texte:

                    ct_mots += 1

                    g = gram(mot, lexicon, ponctuation, stops, noms_propres, passe, fifo, proba_p1)

                    if g == 0: # le mot n'a pas été trouvé dans lexicon
                    # le mot est indéfini, on n'enregistre pas la suite de fonctions grammaticales, on saute au i suivant

                        ct_rejet += 1
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
                    ct_proba += 1
                    fifo.append(g)
                    fifo.popleft()

        print()
        print(ct_proba/ct_mots)

    """
    # produit un fichier des mots rejettés par gram pour voir les failles
    with open(local_path + '/Data/mots_vais.txt', 'w') as f:
        f.write('\n'.join(sorted(mots_vais)))
    """
    # pickle dump des noms propres
    with open(local_path + '\\Data\\Noms_propres.pkl', 'wb') as f:
            pickle.dump(noms_propres, f)

    return proba_p2


def multi_analyse(prof_max):

    local_path = os.path.dirname(__file__)
    with open(local_path + '/Data/Lexicon_simplifié.pkl', "rb") as file:
        lexicon = pickle.load(file)

    # Création dossier Tables de transitions dans Data
    path_nouv_dossier = local_path + '/Data/Tables de transitions'
    if not os.path.exists(path_nouv_dossier):
        os.makedirs(path_nouv_dossier)

    for prof in range(1,prof_max+1):

        print(prof)
        proba_table = analyse(corpus, lexicon, prof, local_path)
        print(list(proba_table.keys())[:10])
        print(len(proba_table.keys()))

        # pickle dump dans Tables de transitions
        name = f"Syntaxe_proba_profondeur_{prof}.pkl"
        with open(local_path + f'\\Data\\Tables de transitions\\{name}', 'wb') as f:
            pickle.dump(proba_table, f)


prof_max = 8
multi_analyse(prof_max)
# analyse(corpus, 5)