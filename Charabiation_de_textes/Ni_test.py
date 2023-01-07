import os, pickle

local_path = os.path.dirname(__file__)

with open(local_path + '/../Data/Lexicon_simplifié.pkl', "rb") as file:
    lexicon = pickle.load(file)

L = lexicon.values()
natures = []

for dico in L :
    natures += dico.keys()

natures = list(sorted(set(natures)))

print(natures)
print(len(natures))