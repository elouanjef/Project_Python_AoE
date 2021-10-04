import time
#from tqdm import tqdm


class Unite:
    
    batiment = False
    soldat = False
    villageois = False
    alive = False
    type = False
    name = False
    resWRGF = [0, 0, 0, 0]

    def __init__(self, name, type):
        self.name = name
        self.type = type
        if str(self.type) in ("cavalerie", "infanterie", "artillerie"):
            self.soldat = True
            self.alive = True
        elif str(self.type) in ("batiment"):
            self.batiment = True
            self.alive = True
        elif str(self.type) in ("villageois"):
            self.villageois = True
            self.alive = True
        else:
            print("Il faut choisir un type valable")

def militaire(nb, troop, type, resWRGF, t):
    # test_resource(resWRGF)
    armee = {}
    for i in range(nb):
        time.sleep(t)
        armee[i] = Unite(troop, type)
        print("Vous avez enrôlé", i + 1, str(troop), "de type", str(type), "pour", resWRGF[0], "de bois",
              resWRGF[1], "de pierre", resWRGF[2], "d'or et", resWRGF[3], "de nourriture")
    return armee

def villager(nb):
    # test_resource(resWRGF)
    villageois = {}
    resWRGF = [0, 0, 0, 50]
    for i in range(nb):
        time.sleep(3)
        villageois[i] = Unite("villageois", "villageois")
        print("Villageois créé pour", resWRGF[3], "de nourriture")
    return villageois

def construire(name, resWRGF, t):
    # test_resource(resWRGF)
    time.sleep(t)
    construction = Unite(name,'batiment')
    print("Vous avez bâti un(e)", str(name), "pour", resWRGF[0], "de bois",
          resWRGF[1], "de pierre", resWRGF[2], "d'or et", resWRGF[3], "de nourriture")
    return construction


#[ WOOD , ROCK , GOLD , FOOD ]
units_res = {
    'archer' : [0, 0, 30, 20],
    'arbaletrier' : [0, 0, 20, 45],
    'mousquetaire' : [0, 0, 70, 30],
    'piquier' : [30, 0, 0, 30],
    'fantassin' : [25, 0, 35, 0],

    'canon_lourd' : [150, 0, 80, 0],
    'couleuvrine'  : [200, 0, 80, 0],

    'chevalier' : [0, 0, 100, 75],
    'uhlan' : [0, 0, 75, 60],


    'centre_ville' : [600, 0, 0, 0],
    'caserne' : [150, 0, 0, 0],
    'usine' : [200, 0, 0, 0],
    'moulin' : [150, 0, 0, 0],
    'eglise' : [250, 0, 0, 0],
    'ecurie'    : [175, 0, 0, 0],
    'plantation' : [800, 0, 0, 0]
}

units_time = {
    'archer' : 3,
    'arbaletrier' : 3,
    'mousquetaire' : 4,
    'piquier' : 4,
    'fantassin' : 5,

    'canon_lourd' : 30,
    'couleuvrine'  : 30,

    'chevalier' : 12,
    'uhlan' : 10,


    'centre_ville' : 60,
    'caserne' : 40,
    'usine' : 40,
    'moulin' : 30,
    'eglise' : 35,
    'ecurie'    : 40,
    'plantation' : 30
}

units_age = {
    'archer' : 1,
    'arbaletrier' : 1,
    'mousquetaire' : 2,
    'piquier' : 1,
    'fantassin' : 2,

    'canon_lourd' : 2,
    'couleuvrine'  : 2,

    'chevalier' : 2,
    'uhlan' : 1,


    'centre_ville' : 1,
    'caserne' : 1,
    'usine' : 2,
    'moulin' : 1,
    'eglise' : 2,
    'ecurie' : 1,
    'plantation' : 2
}

def caserne(nb,troop):
    militaire(nb,troop,'infanterie',units_res[str(troop)],units_time[str(troop)])

def usine(nb,troop):
    militaire(nb,troop,'artillerie',units_res[str(troop)],units_time[str(troop)])

def ecurie(nb,troop):
    militaire(nb,troop,'cavalerie',units_res[str(troop)],units_time[str(troop)])

def batiment(nom):
    construire(nom, units_res[str(nom)], units_time[str(nom)])



caserne(1,"archer")

ecurie(1,'uhlan')

batiment('moulin')

usine(1,'canon_lourd')

villager(3)
