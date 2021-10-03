from typing import Dict
import time
from tqdm import tqdm #pour la barre de progression de recrutement des troupes ou de construction des bâtiments

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
        elif str(self.type) in ("villageois"):
            self.villageois = True
            self.alive = True
        else:
            print("Il faut choisir un type valable")


def militaire(nb,troop,type,resWRGF,t):
    # test_resource(resWRGF)
    armee = {}
    for i in tqdm(range(nb)):
        time.sleep(t)
        armee[i] = Unite(troop,type,resWRGF)
        print("\nVous avez enrôlé",i+1,str(troop), "de type", str(type), "pour", resWRGF[0], "de bois",
              resWRGF[1], "de pierre", resWRGF[2], "d'or et", resWRGF[3], "de nourriture")
    return armee

def villager(nb):
    # test_resource(resWRGF)
    villageois = {}
    resWRGF = [0,0,0,50]
    for i in tqdm(range(nb)):
        time.sleep(3)
        villageois[i] = Unite("villageois","villageois",resWRGF)
        print("\nVillageois créé pour",resWRGF[3],"de nourriture")
    return villageois


#Peut-être rajouter une ligne pour dire combien le batiment met de temps à se construire,
#avec une classe batiments avec tous les temps de construction des batiments, et du coup faire un print(self.temps_construction_eglise) par exemple
def construire(name,type,resWRGF,t):
    #test_resource(resWRGF)
    time.sleep(t)
    construction = Unite(name,type,resWRGF)
    print("\nVous avez bâti un(e)", str(name), "de type", str(type),"pour", resWRGF[0], "de bois",
              resWRGF[1], "de pierre", resWRGF[2], "d'or et", resWRGF[3], "de nourriture")
    return construction

test_villageois = villager(15)
print(test_villageois)
test_archers = militaire(10,"archer","infanterie",[0,0,20,30],3)

test_hotel = construire("caserne","militaire",[200,100,0,0],10)

