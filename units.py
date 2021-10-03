from typing import Dict
import time #pip install time
from tqdm import tqdm  #pip install tqdm

class Unite:

    batiment = False
    soldat = False
    villageois = False
    alive = False
    type = False
    name = False
    resWRGF = [0,0,0,0]

    def __init__(self, name, type, resWRGF):
        self.name = name
        self.type = type
        if str(self.type) in ("cavalerie", "infanterie", "artillerie"):

            self.soldat = True
            self.alive = True
        elif str(self.type) in ("militaire", "economie"):

            self.batiment = True
            self.alive = True
        elif str(self.villageois) in ("villageois"):
            print("Vous avez créé un", str(self.name), "de type", str(self.type))
            self.villageois = True
            self.alive = True
        else: print("Il faut choisir un type valable")

def militaire(nb,troop,type,resWRGF,t):
    armee = {}
    for i in tqdm(range(nb)):
        time.sleep(t)
        armee[i] = Unite(troop,type,resWRGF)
        print("\nVous avez enrôlé",i+1,str(troop), "de type", str(type), "pour", resWRGF[0], "de bois",
              resWRGF[1], "de pierre", resWRGF[2], "d'or et", resWRGF[3], "de nourriture")
    return armee

def construire(name,type,resWRGF,t):
    time.sleep(t)
    construction = Unite(name,type,resWRGF)
    print("\nVous avez bâti un(e)", str(name), "de type", str(type),"pour", resWRGF[0], "de bois",
              resWRGF[1], "de pierre", resWRGF[2], "d'or et", resWRGF[3], "de nourriture")
    return construction

test_archers = militaire(10,"archer","infanterie",[0,0,20,30],3)

test_hotel = construire("caserne","militaire",[200,100,0,0],10)

