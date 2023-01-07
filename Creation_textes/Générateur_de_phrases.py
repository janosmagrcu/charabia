import os, pickle
from random import choices, choice
from math import tau,pi
from num2words import num2words


def chargement(profondeur_max):

	local_path = os.path.dirname(__file__)
	with open(local_path + '/Data/Lexicon_inverse.pkl', "rb") as file:
		lexicon_inv = pickle.load(file)

	proba_tables = [None]*profondeur_max
	for prof in range(profondeur_max):
		with open(local_path + f'/Transitions Tables/Syntaxe_proba_profondeur_{prof+1}.pkl', "rb") as file:
			proba_tables[prof] = pickle.load(file)
		print(f"table prof {prof+1} - {len(proba_tables[prof])} entrées")

	return proba_tables, lexicon_inv

def générer(n_phrases, profondeur, frequence):

	ponctuation = {')', ':', '=','+','!','?',';','-','…','(','}',"'",',','{',']','"','.','['}
	stops = {'.','?','!','…'}

	phrases = ['.']
	n = 0

	while True:

		prof = min(len(phrases),profondeur)

		while True:
			precedents = tuple(phrases[-prof:])
			if precedents not in proba_tables[prof-1]:
				prof -= 1
				if prof==0:	
					print("AAAAAHHHH")
					print(precedents)
					""" si ça arrive, activer les trois lignes suivantes
					générer(n_phrases)
					return
					"""
				continue
			else:
				probas = proba_tables[prof-1][precedents]
				gram = choices(list(probas.keys()), weights = list(probas.values()), k = 1)[0]
				phrases += [gram]
				break

		if gram in stops|{'-'} and phrases[-2] not in stops: 
			n += 1
			if n==n_phrases: break

	# enlever guillemets et parenthèses
	phrases = [p for p in phrases if p not in {"'",'"','(',')','[',']'}]
	# enlever les doubles ponctuations consécutives:
	phrases = [g for i,g in enumerate(phrases[1:]) if not (g in ponctuation-{'-'} and phrases[i-1] in ponctuation)]

	remplacements = {"pasque":"parce que", "onc": "jamais", "because": "parce que", "bicause": "parce que"}
	# à partir d'ici, mots contient des tuples (mot, gram)
	mots = [('.','.')]
	maj = 1
	retour = 0
	for i,gram in enumerate(phrases):

		# les autres ponctuations
		if gram in ponctuation-stops-{"-"}:
			mots = mots[:-1] if gram not in {';',':'} else mots
			mot = gram
		# les ponctu stops
		elif gram in stops:
			if gram == '.': mots = mots[:-1]
			mot = gram + '\n'*(retour or choice([0,0,0,1,0,0,0]))
			maj = 1
			retour = 0
		# les tirets "-"
		elif gram == '-':
			prec = ''.join((m[0] for m in mots[-2:]))
			if "\n" not in prec: mot = "\n- "
			if all(s not in prec for s in stops):
				if mots[-1][0] == ' ': mots.pop()
				mot = '.' + mot
			maj = 1
			retour = choice([1,1,1,1,0])
		# les noms propres
		elif gram =='NPR':
			mot = choice(['Jean-Philippe','Yvonne'])
			maj = 0
		# les nombres
		elif gram=='NUM':

			# à faire : analyser en différenciant 'NUM' et 'ORD'

			num = choices(['42',choice(range(500))], weights = [tau,1])[0]
			mot = choices([num2words(num, lang='fr'),num2words(num, lang='fr', to='ordinal')],weights=[pi,1])[0]
			if maj: mot = mot.capitalize()
			maj = 0
		# les mots
		else:
			mot = choices(list(lexicon_inv[gram].keys()),list(lexicon_inv[gram].values()),k=1)[0]
			# mot = choice(list(lexicon_inv[gram]))
			if mot in remplacements: mot = remplacements[mot]
			if maj: 
				mot = mot.capitalize()
				maj = 0

		mots += [(mot, gram)]
		# les espaces
		if '\n' not in mots[-1][0]:
			mots += [(" "," ")]

	problèmes = {"je","j","l","le","la","d","de","t","te","s","se","qu","que","m","me","n","ne",
	"jusqu","jusque","lorsqu","lorsque","quoiqu","quoique", "parce qu", "parce que",
	"tandis que","tandis qu", "puisque","puisqu", 'afin de', "afin d"}
	voyelles = set("aeiouâàéèêëïîôùûh")

	mots = mots[1:]
	for i,(mot,gram) in enumerate(mots):

		if mot.lower() in problèmes:
			# print("problème")
			# print(mot,end=' ')
			if mot[-1] != 'e': 
				if mot in {'la',"La"}: mot = mot[:-1]
				mot += "e"
			mot_suivant = mots[i+2]
			# print(f'... {mot} ...',end=' ')
			if mot_suivant[0][0] in voyelles:
				mot = mot[:-1] + "'"
				mots[i+1] = ('','')
			else:
				if mot.lower() == "le" and '_f' in mot_suivant[1] or mot_suivant[0] == "Yvonne": 
					# print("-A-",end='')
					mot = mot[:-1]+'a'
			mots[i] = (mot,gram)
			# print(f" + {mots[i+2]}"," --> ", f"{mot}{mots[i+1][0]}{mot_suivant[0]}")

		# sur le même modèle : ce/cet/cette/ces
		if mot.lower() in {"ce","cet"}:
			# print("ce/cet/cette/ces")
			mot_suivant = mots[i+2]
			# print(mot, mot_suivant, end=' ')
			char = mot_suivant[0][0]
			nombre_suivant = "_p" in mot_suivant[1]
			genre_suivant = "_f" in mot_suivant[1]
			if nombre_suivant:
				suff = "s"
			elif genre_suivant:
				suff = "tte"
			elif char in voyelles: 
				suff = "t"
			else:
				suff =''
			mot = mot[:2]+suff
			mots[i] = (mot,gram)
			# print(mot)
			
	print()
	print(''.join(m for m,g in mots))

"""
Yvonne par-derrière endosquelette. Nobiliaire puissamment énergique, la narguait par-dessus embellir desdits myxomatose... Comment, devant concasser, chancela puérilement Jean-Philippe.

Ces frangines racornissent interminablement neutres : ces dynamiques aberrations cavaler. Au portique, extravasation garantit au contemplatif par-dessous schleu galetas. Les théoriquement surprenions de traviole. Tandis qu eux-mêmes tressaillent fors Yvonne.                                                                                                                                                                                                    
-Cessionnaire !                                                                                                                                                                                                                    
-Flatus vocis, abc, los, pékinois, as-rois, plein-temps, mi-porté, saint-crépin, surchoix gourmés, cafardeux revenants, lutz incomplets, vous-mêmes nous-mêmes mourions, enterrions plusieurs concepts épiloguer.    

Car monotonement déraisonnait.                                                                                                                                                                                                     
- Elle-même tellement ?                                                                                                                                                                                                            
Elle-même poquait sous-prieur Yvonne par désarticulant des anémiques impalas dès fatras, au manteau, au maelstrom, des rehauts, des blue jeans, dispatchait insolation, le escarpement si fors il ni onze nord-ouest, eux-mêmes trouveraient depuis Yvonne s dégageraient fâcheusement, subtilement.                                                                                                                                                                  
Diable.                                                                                                                                                                                                                            
Alléluia.                                                                                                                                                                                                                          
Flamand.                                                                                                                                                                                                                           
- Adressage Yvonne, pécore au saloir stroboscopique, le Jean-Philippe versus Jean-Philippe, au sloughi ils gémissaient pieusement puis gloussaient dans cette joie carotteuse péniblement réclamait procès-verbal.                 
"""

profondeur_max = 6
print("Chargement des tables de transitions ...")
proba_tables, lexicon_inv = chargement(profondeur_max)

while True:
	print()
	profondeur = int(input("Quelle profondeur ? "))
	n = int(input("combien de phrases ? "))
	frequence = input("utilisation de la fréquence (0/1) ? ")
	générer(n,profondeur,frequence)
