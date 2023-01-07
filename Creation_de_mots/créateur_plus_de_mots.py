import codecs, unicodedata, os


local_path = os.path.dirname(__file__)

with codecs.open(local_path+'/Data/mots_TD.txt', "r", "utf-8") as file:
    texte = ''.join(unicodedata.normalize('NFC', line) for line in file.readlines())
    texte = texte.split()

mots_de_mots_TD = {mot for mot in texte}


with codecs.open(local_path+'/Data/liste.de.mots.francais.frgut.txt', "r", "utf-8") as file:
    texte = ''.join(unicodedata.normalize('NFC', line) for line in file.readlines())
    texte = texte.split()

mots_de_gut = {mot for mot in texte}

union = mots_de_mots_TD | mots_de_gut

mots_en_plus = {mot for mot in mots_de_mots_TD if mot not in mots_de_gut}

print(mots_en_plus, len(mots_en_plus))

with open(local_path + '/Data/plus_de_mots_fr.txt', 'w') as f:
        f.write('\n'.join(sorted(union)))