import os, pickle
from random import choices, choice, gauss
from num2words import num2words


def chargement(profondeur_max, avec_nltk):

	local_path = os.path.dirname(__file__)
	with open(local_path + '/../Data/Lexicon_inverse.pkl', "rb") as file:
		lexicon_inv = pickle.load(file)

	proba_tables = [None]*profondeur_max
	for prof in range(profondeur_max):
		with open(local_path + f'/../Data/Probas/Creation_textes_{("","nltk_")[avec_nltk]}Proba_profondeur_{prof+1}.pkl', "rb") as file:
			proba_tables[prof] = pickle.load(file)
		print(f"table prof {prof+1} - {len(proba_tables[prof])} entrées")

	return proba_tables, lexicon_inv

def générer(n_phrases, profondeur, frequence):

	ponctuation = '):=+!?;-…(}\',{]".['
	stops = '.?!…'

	# Tout d'abord on part d'un point et on génère des squelettes grammaticaux de phrases
	# en utilisant les probas de transition

	squelette = ['.']
	n = 0
	sécurité = 0
	while True:
		
		sécurité += 1
		if sécurité > 10000: # pour éviter de rares boucles sans ponctuations
			générer(n_phrases, profondeur, frequence)
			return

		prof = min(len(squelette),profondeur)

		while True:
			precedents = tuple(squelette[-prof:])
			if precedents not in proba_tables[prof-1]:
				prof -= 1
				continue
			else:
				probas = proba_tables[prof-1][precedents]
				gram = choices(list(probas.keys()), weights = list(probas.values()), k = 1)[0]
				squelette += [gram]
				break

		if gram in stops:
			n += 1
			if n==n_phrases: break

	# A ce stade on a les squelettes de phrases, avec ponctuations mais pas les espaces.

	remplacements = {"pasque":"parce que", "onc": "jamais", "because": "parce que", "bicause": "parce que", "=TRUE()": 'un'}

	phrases = []
	maj = 1 # prévision d'une majuscule pour le mot suivant
	retour = 1 # prévision d'un retour à la ligne après le prochain stop
	espace = 0 # prévision d'un espace avant l'élément suivant

	# Pour chaque gram, on remplace par un élément approprié : ponctuation, nombre, mot, etc ...
	for i,gram in enumerate(squelette):

		if gram in ponctuation:
			e = gram
			if gram in ':=+!?;-…(}{]"[':
				e = ' ' + e
				espace = 1
			if gram in stops:
				retour = retour or choice([0,0,0,1,2,1,1,0,0,0,0,0])
				e = e + '\n'*retour
				espace = not retour
				maj = 1
				retour = 0

		elif gram == 'DIA':
			e = '\n-'
			espace = 1
			maj = 1
			retour = choice([1,1,1,1,1,0])

		elif gram == 'NPR':
			e = ['',' '][espace==1] + choice(['Jean-Philippe','Yvonne'])
			if e.strip() == 'Yvonne': gram = "_f"
			maj = 0
			espace = 1

		elif gram in {'ADJ:num','ORD'}:
			num = abs(int(choice([42,gauss(1,8),42,1,2,gauss(1,70),gauss(1,8),1,42,gauss(1,8)])))
			num = num2words(num, lang='fr') if gram == 'ADJ:num' else num2words(num, lang='fr', to='ordinal')
			if maj:
				num = num.capitalize()
				maj = 0
			e = ['',' '][espace==1] + num
			espace = 1

		elif gram in {'ne','ni'}:
			e = gram
			if maj:
				e = mot.capitalize()
				maj = 0
			e = ['',' '][espace==1] + e
			espace = 1
		else:
			# choix d'un mot à partir de gram dans le lexicon inversé
			if frequence:
				mot = choices(list(lexicon_inv[gram].keys()),list(lexicon_inv[gram].values()),k=1)[0]
			else: 
				mot = choice(list(lexicon_inv[gram]))
			if mot in remplacements: mot = remplacements[mot]
			if maj:
				mot = mot.capitalize()
				maj = 0
			e = ['',' '][espace==1] + mot
			espace = 1

		phrases += [(e,gram)]

	phrases = phrases[1:]

	# problèmes d'apostrophes devant les voyelles ...
	problèmes = {"je","j","l","le","la","d","de","t","te","s","se","qu","que","m","me","n","ne",
	"jusqu","jusque","lorsqu","lorsque","quoiqu","quoique", "parce qu", "parce que",
	"tandis que","tandis qu", "puisque","puisqu", 'afin de', "afin d", "est-ce qu", "est-ce que"}
	voyelles = "aeioâàéèêëïîôùûhu" # le u est à la fin à cause de qu', jusqu', etc. Il est enlevé
								  # lorsqu'on s'intéresse à la fin du mot précédent

	for i,(mot,gram) in enumerate(phrases[:-1]):

		mot_striped_lowered = mot.strip().lower()

		if mot_striped_lowered in problèmes:

			fin_prec = mot[-1]
			deb_suiv = phrases[i+1][0].strip()[0]

			if fin_prec in voyelles[:-1] and deb_suiv in voyelles:
				# mot précédent terminé par voyelle, et le suivant débute par une voyelle
				mot = mot[:-1]+"'"
				phrases[i+1] = (phrases[i+1][0].lstrip(),phrases[i+1][1])

			elif fin_prec not in voyelles[:-1] and deb_suiv not in voyelles:
				# mot précédent terminé par consonne, et le suivant débute 
				# par une consonne ou est une ponctuation
				gram_suiv = phrases[i+1][1]
				if "_f" in gram_suiv: # il faudrait restreindre à certains mots de problèmes
					mot = mot + "a"
				else:
					mot = mot + "e"

			elif fin_prec not in voyelles[:-1] and deb_suiv in voyelles:
				# mot précédent terminé par une consonne et le suivant
				# débute par une voyelle
				mot = mot + "'"
				phrases[i+1] = (phrases[i+1][0].lstrip(),phrases[i+1][1])

			phrases[i] = (mot,gram)

		# cas particuliers de ce/cet/cette/ces
		if mot_striped_lowered in {"ce", "cet", "cette", "ces"}:

			mot_suivant, gram_suiv = phrases[i+1]
			# on définit pour le mot suivant :
			fem = "_f" in gram or "_f" in gram_suiv
			plur = "_p" in gram_suiv
			voy = mot_suivant.strip()[0] in voyelles
			espace = ['',' '][mot[0] == ' ']
			maj = mot.strip() != mot_striped_lowered

			if plur:
				mot = 'ces'
			elif fem:
				mot = 'cette'
			else:
				if voy:
					mot = 'cet'
				else:
					mot = 'ce'
			mot = espace + [mot,mot.capitalize()][maj]
			phrases[i] = (mot,gram)

		# cas particuliers de ma/mon (féminin, liaison) ex : on dit mon oie alors que oie = féminin
		if mot.strip().lower() == "ma": # on restrippe et lowere, 
			# parce que le ma peut venir du premier if 
			if phrases[i+1][0].strip()[0] in voyelles:
				espace = ['',' '][mot[0] == ' ']
				maj = mot.strip() == 'Ma'
				mot = espace + ['mon','Mon'][maj]
				phrases[i] = (mot,gram)

		# cas particulier 'de le' -> 'du'
		if mot.strip().lower() == 'le': # on s'intéresse à de le lorqu'on est sur le et non sur de
			if phrases[i-1][0].strip().lower() == 'de':
				espace = ['',' '][phrases[i-1][0][0] == ' ']
				maj = phrases[i-1][0].strip() == 'De'
				mot = espace + ['du', 'Du'][maj]
				phrases[i] = ('','')
				phrases[i-1] = (mot,gram)

		# au / à l' (serait à faire)

	print()
	print(''.join(e for e,g in phrases))


profondeur_max = 15
avec_nltk = 0
print("Chargement des tables de transitions ...")
proba_tables, lexicon_inv = chargement(profondeur_max,avec_nltk)

while True:
	print()
	while True:
		try: 
			profondeur = int(input(f"Quelle profondeur ? (1 à {profondeur_max}) "))
			if 0 < profondeur <= profondeur_max: break
			else: print(f"Non, entre 1 et {profondeur_max} !!!")
		except: print("Essaie encore")
	while True:
		try: 
			n = int(input("combien de phrases ? (1 à 500) "))
			if 0 < n < 500: break
			else:
				print('entre 1 et 500 !')
		except: print("Essaie encore")
	while True:
		try: 
			frequence = int(input("utilisation de la fréquence (0/1) ? "))
			if frequence in (0,1): break
			else: print("juste 0 ou 1 s'il te plaît.")
		except: print("Essaie encore")

	générer(n,profondeur,frequence)