import os
import numpy as np

#import codecs


filepath = "mots_francais.txt"

count = np.zeros((256,256,256),dtype='int32')
res = []

with codecs.open(filepath, "r", "utf-8") as lines:
    for l in  lines:
        i=0
        j=0
        for k in [ord(c) for c in list(l)]:
            count[i,j,k] += 1
            i = j
            j = k
count.tofile("count2D.bin")

#import numpy as np
from numpy.random import choice
#import codecs

# Build a dictionnary to check whether word already exists
filepath = "mots_francais.txt"
dico = []
with codecs.open(filepath, "r", "utf-8") as lines:
    for l in  lines:
        dico.append(l[:-1])
 
# Load the trigram count matrixand normalize it     
count = np.fromfile("count2D.bin",dtype="int32").reshape(256,256,256)
s=count.sum(axis=2)
st=np.tile(s.T,(256,1,1)).T
p=count.astype('float')/st
p[np.isnan(p)]=0

non = 12
if non == 1:
    # Build words
    outfile = "output.txt"
    f = codecs.open(outfile,"w","utf-8")

    # How many for each target size

    min,max = 3,10
    nv_mots = [[]]*(max-min)
    K = 100
    for TGT in range(min,max):
        total = 0
        while total<100:
            i=0
            j=0
            res = u''
            while not j==10:
                k=choice(range(256),1,p=p[i,j,:])[0]
                res = res + chr(k)
                i=j
                j=k
            if len(res) == 1+TGT:
                if res[:-1] in dico:
                    x=res[:-1]+"*"
                else:
                    x=res[:-1]
                total += 1
                nv_mots[len(res)-1-min].append(x)
                f.write(x+"\n")
    f.close()

    import random as rd

    phrase = '' 
    for _ in range(20):
        u = rd.randint(0,5-min)
        l = rd.randint(0,10)
        v = rd.randint(6-min,max-min-1)
        phrase += f'{nv_mots[u][l]} {nv_mots[v][l]} '
    print(nv_mots)

text = ' '
for _ in range(100): text = np.random.choice(letters,p=p[letters.index(text[0])][:alpha]) + text