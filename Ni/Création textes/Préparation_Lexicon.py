import os
import pickle
from openpyxl import load_workbook
from num2words import num2words

"""
Création d'un fichier pickle contenant un dictionnaire réduit à partir du Lexicon
col 1 - orthographe
col 2 - gram_genre_nombre_infover

Prend une vingtaine de secondes
"""

local_path = os.path.dirname(__file__)
wb = load_workbook(local_path + "/Data/Lexique383 - propre.xlsx")
sheet = wb.active

lexicon = {}

for i,row in enumerate(sheet.iter_rows(min_row=2)):
	ortho, gram, genre, nombre, infover = row
	ort,gra,gen,nbr,ivs = ortho.value,gram.value,genre.value,nombre.value,infover.value
	
	ivs = {iv for iv in ivs.split(';')if iv} if ivs else ('',)

	for iv in ivs:
		if iv=='' or 'par' in iv:
			g = '_'.join([e for e in (gra,gen,nbr,iv) if e])
		else:
			g = '_'.join([e for e in (gra,iv) if e])

		lexicon[ort] = lexicon.get(ort,[]) + [g]

# ajout des NUM et ORD de 0 à 1000:

for n in range(1001):
	lexicon[num2words(n, lang='fr')] = ['NUM']
	lexicon[num2words(n, lang='fr', to='ordinal')] = ['ORD']

# lexicon inverse :

lexicon_inv = {}

for mot,gram in lexicon.items():
	for g in gram:
		lexicon_inv[g] = lexicon_inv.get(g,set()) | {mot}

# pickle dump
with open(local_path + '/Data/Lexicon_simplifié.pkl', 'wb') as f:
    pickle.dump(lexicon, f)

with open(local_path + '/Data/Lexicon_inverse.pkl', 'wb') as f:
    pickle.dump(lexicon_inv, f)