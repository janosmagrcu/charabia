import codecs, unicodedata, os, pickle, random

"""
Code pas du tout fini

Objectif : prendre un extrait d'un livre parmis les Goncourts, et remplacer quelques mots de cet extrait par du charabia
Mais du charabia précis : créé à partir de mots de la même nature que le mot remplacé
"""

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
    

def trouveur_extrait(n_mots, année_voulue, local_path):
    """
    renvoie un extrait de n_phrases du livre dont l'année est la plus proche de l'année voulue
    """
    noms_livres = os.listdir(local_path+'/Data/Collection Prix Goncourt/txt')
    années = [nom_livre[:4] for nom_livre in noms_livres]
    années_diff = []
    for i,année in enumerate(années) :
        années_diff += [(abs(année_voulue - int(année)), i)]
    titre_voulu = noms_livres[min(années_diff)[1]]
    
    with codecs.open(local_path+'/Data/Collection Prix Goncourt/txt/'+titre_voulu, "r", "utf-8") as file:
        texte = ''.join(unicodedata.normalize('NFC', line) for line in file.readlines())

    # réutiliser nettoyage Goncourt avec tous les caractères moisis
    # rajouter espace avant et après ponctuations
    # split sur les espaces => liste de mots et ponctuations
    # len(tout ça) puis randint comme j'ai fait, sur 

    # limitation du nombre de mots :
    n_mots_max = 1000
    n_mots = min(n_mots_max, n_mots)
    i_début_extrait = random.randint(0, (2/3)*(len(texte)-2000)-n_mots_max)

    extrait = texte[i_début_extrait, i_début_extrait + n_mots]

    return titre_voulu

print(trouveur_extrait(5, 1940, os.path.dirname(__file__)))

def charabieur_mots(mots_à_remplacer):
    """
    retourne la liste de mots à remplacer
    """
    # on pourrait interdire la charabiation de certaines natures (comme les déterminants)
    pass




def charabieur(n_mots, année_voulue = 0):

    # tables de transition
    # noms propres
    # ponctuation
    # stops => vérifier qu'on l'a utilisé
    # un texte
    # lexicon
    # lexicon inverse
    # num2text
    # charabia

    local_path = os.path.dirname(__file__)

    ponctuation = {')', ':', '=','+','!','?',';','-','…','(','}',"'",',','{',']','"','.','['}

    stops = {'.','?','!','…'} # peut-être qu'on n'en a pas besoin, à voir
    
    with open(local_path + '/Data/Noms_propres.pkl', "rb") as file:
        noms_propres = pickle.load(file)
    
    with open(local_path + '/Data/Lexicon_simplifié.pkl', "rb") as file:
        lexicon = pickle.load(file)

    with open(local_path + '/Data/Lexicon_inverse.pkl', "rb") as file:
        lexicon_inv = pickle.load(file)

    extrait = trouveur_extrait(n_mots, année_voulue, local_path) # liste sûrement

    for mot in extrait :
        if len(mot) <8 :
    
            pass



charabieur(5,1789)








# Prendre un morceau de texte dans les Goncourts, prend en entrée l'année et le nombre de phrases
# Importer le fichier
# Prendre la taille du livre (un peu moins), choisir un caractère au hasard
# Identifier un passage propre, attenton : si conditions jamais rencontrées

# Nettoyage goncourt : garder une partie de l'autre code

# Choisir les mots à remplacer : assez long et gram unique ou intersection unique : copier code proba et importer les probas

# Pour chaque mot à remplacer, charabier un mot de même nature et le mettre à la place : lexicon inverse et le code de charabia

# Remise en forme lisible du texte