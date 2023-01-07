import os, pickle

local_path = os.path.dirname(__file__)

with open(local_path + '/../Data/Probas/Probas_inv.pkl', 'wb') as f:
    pickle.dump({'nimporte quoi':6}, f)