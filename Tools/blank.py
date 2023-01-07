import matplotlib.pyplot as plt
import statistics as stat
import math

with open('mots_francais.txt','r',-1,'utf-8') as mots:
    with open('mots_jonas.txt','r',-1,'utf-8') as jonas:
        with open('mots_joseph.txt','r',-1,'utf-8') as joseph:
            lenlist_fr = [0]*70
            lenlist_jon = [0]*70
            lenlist_jos = [0]*70
            X = [i+1 for i in range(70)]
            for m in mots: lenlist_fr[len(m[:-1])] += 1
            for m in jonas: lenlist_jon[len(m[:-1])] += 1
            for m in joseph: lenlist_jos[len(m[:-1])] += 1
            data = []
            data_jon = []
            data_jos = []
            for i in X: 
                data += [i]*lenlist_fr[i-1]
                data_jon += [i]*lenlist_jon[i-1]
                data_jos += [i]*lenlist_jos[i-1]
            l = len(data)
            l_jon = len(data_jon)
            l_jos = len(data_jos)
            mu = stat.fmean(data)
            sigma = stat.pstdev(data,mu)
            #print(mu,sigma)
            N = lambda x : math.exp(-0.5*((x-mu)/sigma)**2)/(sigma*math.sqrt(2*math.pi))
            N = [N(i) for i in X]
            A = [n/l for n in lenlist_fr]
            B = [n/l_jon for n in lenlist_jon]
            C = [n/l_jos for n in lenlist_jos]

            data_exp = [31953,95181,58882,55924,41093,34890,28556,19778,12263,6703,3088,1559,699,282,108,51,4,7,1,1,1,3,3,1,1,0,0,0,0,0]+[0]*40
            s = sum(data_exp)
            D = [n/s for n in data_exp]

            plt.plot(X,B,X,D)
            plt.show()
