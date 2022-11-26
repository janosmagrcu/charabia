consonnes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v',  'w', 'x', 'z']
voyelles = ['a', 'e', 'i', 'o', 'u', 'y']
term = {}
term['present'] = {}
term['futur'] = ['ai', 'as', 'a', 'ons', 'ez', 'ont']
term['imparfait'] = {}
term['simple'] = {}


term['present'][1] = ['e', 'es', 'e', 'ons', 'ez', 'ent']
term['present'][2] = ['s', 's', 't', 'ons', 'ez', 'ent']
term['present'][4] = ['iens', 'iens', 'ient', 'enons', 'enez', 'iennent']
term['present'][3] = ['s', 's', '', 'ons', 'ez', 'ent']
term['present'][5] = ['ux', 'ux', 'ut', 'ons', 'ez', 'ent']

term['imparfait'][1] = ['ais', 'ais', 'ait', 'ions', 'iez', 'aient']
term['imparfait'][2] = ['ais', 'ais', 'ait', 'ions', 'iez', 'aient']
term['imparfait'][3] = ['ais', 'ais', 'ait', 'ions', 'iez', 'aient']
term['imparfait'][4] = ['enais', 'enais', 'enait', 'enions', 'eniez', 'enaient']
term['imparfait'][5] = ['ais', 'ais', 'ait', 'ions', 'iez', 'aient']

avoir = {}
avoir['present'] = ['ai', 'as', 'a', 'avons', 'avez', 'ont']

term['simple'][1] = ['ai', 'as', 'a', 'ames', 'ates', 'èrent']
term['simple'][2] = ['is', 'is', 'it', 'imes', 'ites', 'irent']
term['simple'][3] = ['is', 'is', 'it', 'imes', 'ites', 'irent']
term['simple'][4] = ['ins', 'ins', 'int', 'inmes', 'intes', 'inrent']
term['simple'][5] = ['s', 's', 't', 'mes', 'tes', 'rent']



import random

class Verbe():

    def __init__(self, verbe):
        self.verbe = verbe
    

    def rad_grp(self):
        self.lettre_cachee_sing = ''
        self.lettre_vocalique_1_2 = ''
        self.lettre_vocalique_3 = ''
        self.lettre_vocalique_4_5 = ''
        self.lettre_vocalique_6 = ''
        self.lettre_cachee_plur = ''
        self.ton_part = ''
        self.part_pass = ''
        self.term = ''
        if self.verbe[-2:] == 'er': #manger
            self.rad = self.verbe[:-2]
            self.grp = 1 
            self.ton_part = 'é'
            self.part_pass = self.rad + self.ton_part
            self.term = 'er'
            return None
        elif self.verbe[-2:] == 'ir':
            if self.verbe[-3:] == 'oir': 
                self.term = 'oir'
                rd_int_2 = random.randint(0,1)
                if rd_int_2 == 0 or len(self.verbe) < 6: #voir
                    self.rad =  self.verbe[:-2]
                    self.grp = 2
                    self.lettre_vocalique_1_2 = 'i'
                    self.lettre_vocalique_6 = 'i'
                    self.lettre_cachee_plur = 'y'
                    self.lettre_vocalique_3 = 'i'
                    self.ton_part = 'u'
                    self.part_pass = self.verbe[:-3] + self.ton_part
                    return None
                if rd_int_2 == 1:  #vouloir
                    self.grp = 5
                    self.rad = self.verbe[:-3]
                    while self.rad[-1] in consonnes: 
                        self.lettre_cachee_plur += self.rad[-1]
                        self.rad = self.rad[:-1]
                    if self.rad[-1] == 'u':
                        self.rad = self.rad[:-1]
                        self.lettre_vocalique_6 = 'u'
                        self.lettre_vocalique_4_5 = 'u'
                    while self.rad[-1] in voyelles:
                        if self.rad[-1] == 'o':
                            self.rad = self.rad[:-1] 
                            self.lettre_vocalique_1_2 = 'e'
                            self.lettre_vocalique_6 = 'e' + self.lettre_vocalique_6
                            self.lettre_vocalique_4_5 = 'o' + self.lettre_vocalique_4_5
                        else:
                            self.lettre_vocalique_4_5 = self.rad[-1] + self.lettre_vocalique_4_5
                            self.lettre_vocalique_6 = self.rad[-1] + self.lettre_vocalique_6
                            self.lettre_vocalique_1_2 = self.rad[-1] + self.lettre_vocalique_1_2
                            self.lettre_vocalique_3 = self.rad[-1] + self.lettre_vocalique_3
                            self.rad = self.rad[:-1]
                self.ton_part = 'u'
                self.part_pass = self.rad + self.ton_part
                return None
            elif self.verbe[-4:] == 'enir': #venir
                self.term = 'enir'
                self.rad = self.verbe[:-4]
                self.grp = 4
                self.lettre_cachee_plur = ''
                self.ton_part = 'u'
                self.part_pass = self.rad + 'en' + self.ton_part
                return None
            elif self.verbe[-4:] == 'ntir': #sentir, mentir
                self.rad = self.verbe[:-3]
                self.lettre_cachee_plur = 't'
                self.grp = 2
                self.ton_part = 'i'
                self.part_pass = self.rad + 't' + self.ton_part
                return None
            elif self.verbe[-6:] == 'eillir': #cueillir
                self.term = 'ir'
                self.grp = 1
                self.rad = self.verbe[:-2]
                self.lettre_cachee_plur = ''
                self.ton_part = 'i'
                self.part_pass = self.rad + self.ton_part
                return None
            elif self.verbe[-3:] == 'uir':  #fuir
                self.term = 'ir'
                self.grp = 2
                self.rad = self.verbe[:-2]
                self.lettre_cachee_plur  = 'y'
                self.lettre_vocalique_6 = 'i'
                self.lettre_vocalique_1_2 = 'i'
                self.lettre_vocalique_3 = 'i'
                self.part_pass = self.rad + 't'
                return None
            else:
                rd_int = random.randint(0,3)
                self.term = 'ir'
                if rd_int in [0,1] or self.verbe[-3] == 'a': #hair
                    self.rad = self.verbe[:-1]
                    self.grp = 2
                    self.lettre_cachee_plur = 'ss'
                else: 
                    self.rad = self.verbe[:-2] 
                    self.lettre_cachee_plur = ''
                    if rd_int == 3:
                        self.grp = 2
                    elif rd_int == 2: 
                        self.grp = 1
                    if self.verbe[-3]  == self.verbe[-4]: #courir
                        self.rad = self.verbe[:-4]
                        self.lettre_cachee_plur = self.verbe[-4]
                if self.rad[-1] in voyelles:
                    self.part_pass = self.rad + 't'
                else:
                    self.part_pass = self.rad + 'u'
                return None
        elif self.verbe[-3:] == 'tre':
            self.term = 're'
            if self.verbe[-5:] == 'aitre' or self.verbe[-5:] == 'oitre' or self.verbe[-5:] == 'eitre':  #naitre
                self.rad =  self.verbe[:-3]
                self.grp = 2
                self.lettre_cachee_plur = 'ss'
                self.ton_part = 'u'
                self.part_pass = self.rad + self.ton_part
                return None
            else:
                self.rad = self.verbe[:-3] 
                self.grp = 2
                self.part_pass = self.rad + self.ton_part
                if self.verbe[-4] == 't': #battre
                    self.lettre_cachee_plur = 'tt'
                    self.lettre_cachee_sing = 't'
                    self.rad = self.verbe[:-4]
                    self.ton_part = 'u'
                    self.part_pass = self.rad + 'tt' + self.ton_part
                    return None
                return None
        elif self.verbe[-3:] == 'dre':
            self.term = 're'
            if self.verbe[-5:] == 'indre': #teindre
                self.term = 'ndre'
                self.rad = self.verbe[:-4]
                self.grp = 2
                self.lettre_cachee_sing = ''
                self.lettre_cachee_plur = 'gn'
                self.lettre_vocalique_1_2 = 'n'
                self.lettre_vocalique_3 = 'n'
                self.part_pass = self.rad + 'nt'
                return None
            else:
                self.rad = self.verbe[:-3] #vendre
                self.grp = 3
                self.lettre_cachee_plur = 'd'
                self.lettre_cachee_sing = 'd'
                self.ton_part = 'u'
                self.part_pass = self.verbe[:-2] + self.ton_part
                return None
        elif self.verbe[-3:] == 'ire':
            if self.verbe[-4:] == 'oire': #croire
                self.term = 'oire'
                self.rad = self.verbe[:-3]
                self.grp = 2
                self.lettre_cachee_plur  = 'y'
                self.lettre_vocalique_6 = 'i'
                self.lettre_vocalique_1_2 = 'i'
                self.lettre_vocalique_3 = 'i'
                self.ton_part = 'u'
                self.part_pass = self.verbe[:-4] + self.ton_part
                return None
            self.term = 'ire'
            if self.verbe[-4:] == 'aire':
                self.term ='aire'
            self.rad = self.verbe[:-2]
            self.grp = 2
            self.lettre_cachee_plur = 's'
            rd_int_3 = random.randint(0,1)
            if rd_int_3:
                self.ton_part = 'u'
            else:
                self.ton_part = 'it'
            self.part_pass = self.verbe[:-3] + self.ton_part
            return None
        else: #corrompre
            self.term = 're'
            self.rad = self.verbe[:-2]
            self.grp = 2
            self.lettre_cachee_plur = ''
            if self.verbe[-3] == self.verbe[-4]:
                self.lettre_cachee_plur = self.verbe[-4]
                self.rad = self.verbe[:-3]
            self.ton_part = 'u'
            self.part_pass = self.rad + self.ton_part
            return None

    def present(self, pers, nb):
        global term
        if nb == 'plur':
            pers += 3
            if pers == 6:
                if self.lettre_cachee_plur == 'y':
                    return self.rad + self.lettre_vocalique_6 + term['present'][self.grp][pers - 1]
                else:
                    return self.rad + self.lettre_vocalique_6 + self.lettre_cachee_plur + term['present'][self.grp][pers - 1]
            return self.rad + self.lettre_vocalique_4_5 + self.lettre_cachee_plur + term['present'][self.grp][pers - 1]
        else:
            if pers != 3:
                return self.rad + self.lettre_vocalique_1_2 + self.lettre_cachee_sing + term['present'][self.grp][pers - 1]
            else:
                return self.rad + self.lettre_vocalique_3 +  term['present'][self.grp][pers - 1]

    def futur(self, pers,  nb, cond = False):
        global term
        if nb == 'plur':
            pers += 3
        if self.verbe[-2:] == 'er' or 'ir':
            if self.grp == 4:
                futur = self.rad + 'iendr'
            elif self.grp == 5:
                if 'a' in self.lettre_vocalique_4_5:
                    futur = self.rad + 'audr'
                else:
                    futur = self.rad + self.lettre_vocalique_4_5 + 'dr'
            elif self.lettre_cachee_plur == 'y':
                if pers == 6:
                    futur = self.rad + self.lettre_cachee_plur +'er'
                else:
                    futur = self.rad + 'ier'
            else:
                futur = self.verbe
        if self.verbe[-2:] == 're':
            futur = self.verbe[:-1]
        if cond:
            return futur + term['imparfait'][1][pers - 1]
        return futur + term['futur'][pers - 1]
    

    def mod(self):
        mod = ''
        if self.rad[-1] == 'g':
            mod = 'e'
        return mod

    def imparfait(self, pers, nb):
        if nb =='plur':
            pers += 3
        imparfait = self.rad
        if pers not in [4,5]:
            imparfait += self.mod()
        return imparfait + self.lettre_vocalique_4_5 + self.lettre_cachee_plur + term['imparfait'][self.grp][pers - 1]

    def tps_comp(self, tps, pers, nb):
        if nb == 'plur':
            pers += 3
        if tps == 'passe':
            return avoir['present'][pers - 1] + ' ' + self.part_pass

        
    def passe_simple(self, pers, nb):
        if nb == 'plur':
            pers += 3
        if self.grp == 1 or self.grp ==4:
            return self.rad + self.mod() + term['simple'][self.grp][pers - 1]
        simple = self.rad
        if self.grp == 3 or self.term == 'ndre' or len(self.lettre_cachee_plur) == 2 and self.lettre_cachee_plur != 'ss': 
            simple += self.lettre_cachee_plur
        else:
            n = len(self.term)
            simple = self.verbe[:-n]
        return simple + term['simple'][self.grp][pers - 1]



abattre = Verbe('indonorionneraire')
abattre.rad_grp()
print(abattre.present( 1, 'plur'))
print(abattre.grp, abattre.lettre_cachee_plur, abattre.lettre_vocalique_1_2, abattre.lettre_vocalique_4_5,  abattre.rad)


