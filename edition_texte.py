# pour transformer un document texte quelconque en document normalisé exploitable (enregistré sous nom__.txt)
def clean(url):
    with open(url,'r') as mots_in:
        with open(url[:-4]+'__.txt','x') as mots_out:
            text = ''
            for m in mots_in: text += m
            text = text.lower().strip().replace('  ',' ').replace(' ','\n').replace('\n\n','\n').replace('.','')
            mots_out.write(text)

# pour transformer un document exploitable en liste de mots
def wlist(url):
    with open(url,'r') as mots:
        wstr =''
        for m in mots: wstr += m[:-2]+'%'
        assert (' ' not in wstr) and ('\n' not in wstr), 'texte pas normalisé'
        return wstr.split(sep='%')

# pour extraire d'une liste de mots une répartition des longueurs de mots
def lengths(wlist):
    Max = 0
    for w in wlist: 
        if len(w) > Max: Max = len(w)
    Max = max(Max,30)
    lenlist = [0]*Max
    X = [i+1 for i in range(Max)]
    for m in wlist: lenlist[len(m[:-1])] += 1
    return lenlist

# pour grapher une répartition de longueurs de mots
# la modéliser (normale=True et/ou expo=True)
# la comparer à celle d'un dictionnaire (comp=dico) ou d'un texte (comp=text)
def stat(url,comp=None,normale=False,expo=False):
    import matplotlib.pyplot as plt
    import statistics as stat
    import math

    lenlist = lengths(wlist(url))
    Max = len(lenlist)

    #print(wlist(url))

    X = [i+1 for i in range(Max)]
    data = []
    for i in X: data += [i]*lenlist[i-1]
    l = len(data)
    mu = stat.fmean(data)
    sigma = stat.pstdev(data,mu)
    #print(f'mu = {mu}, sigma = {sigma}')
    A = [n/l for n in lenlist]

    if normale == True:
        N = lambda x : math.exp(-0.5*((x-mu)/sigma)**2)/(sigma*math.sqrt(2*math.pi))
        Y = [N(i) for i in X]
        plt.plot(X,Y,label=f'Normale mu={round(mu,1)} sigma={round(sigma,2)}')

    if expo == True:
        alpha = 1/sigma
        E = lambda x : alpha*math.exp(-x*alpha)
        Z = [E(i) for i in X]
        plt.plot(X,Z,label=f'Exponentielle lambda={1/sigma}')


    if comp == 'dico':
        lenlist_dico = lengths(wlist('mots_francais.txt'))
        l_dico = sum(lenlist_dico)
        C = [n/l_dico for n in lenlist_dico]
        plt.plot(X,C,label='Dictionnaire')


    if comp == 'text':
        # les chiffres viennent du site : http://linguistiques.muroni.free.fr/linguistiques/longueurdesmots.html
        # pas hésiter à aller voir le site Hyperbase pour des grosses bases de données textuelles plurilingues
        lenlist_text = [31953,95181,58882,55924,41093,34890,28556,19778,12263,6703,3088,1559,699,282,108,51,4,7,1,1,1,3,3,1,1,0,0,0,0,0]+[0]*(Max-30)
        l_text = sum(lenlist_text)
        B = [n/l_text for n in lenlist_text]
        plt.plot(X,B,label='Texte')

    plt.plot(X,A,label=url)
    plt.xlabel('taille du mot')
    plt.ylabel('Probabilité')
    plt.title(f'Taille des mot dans <{url}>')
    plt.legend()
    plt.show()




