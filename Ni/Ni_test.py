import os, pandas as pd

local_path = os.path.dirname(__file__)

df = pd.read_pickle(local_path + '/Data/Lexicon_simplifié.pkl')

e = df.iloc[5]['ortho']

print(e)

