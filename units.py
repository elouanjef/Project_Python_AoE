from typing import Dict

class Unite:

    batiment = False
    soldat = False
    villageois = False
    alive = False
    type = False
    name = False
    costw = 0
    costf = 0
    costg = 0
    costr = 0

    def attributs(self,costw,costr,costg,costf):
        self.costw = costw
        self.costr = costr
        self.costg = costg
        self.costf = costf
        if self.soldat:
            print("Unité ajoutée !",str(self.name),"vaut :",costw,"bois",costr,"pierre",costg,"or",costf,"nourriture")
        elif self.batiment:
            print("Bâtiment ajouté !",str(self.name),"vaut :",costw,"bois",costr,"pierre",costg,"or",costf,"nourriture")
        elif self.villageois:
            print("Villageois ajouté !", str(self.name), "vaut :", costw, "bois", costr, "pierre", costg, "or", costf,
                  "nourriture")

    def __init__(self, name, type):
        self.name = name
        self.type = type
        if str(self.type) in ("cavalerie", "infanterie", "artillerie"):
            print("Vous avez enrôlé un(e)", str(self.name), "de type", str(self.type))
            self.soldat = True
            self.alive = True
        elif str(self.type) in ("militaire", "economie"):
            print("Vous avez bâti un(e)", str(self.name), "de type", str(self.type))
            self.batiment = True
            self.alive = True
        elif str(self.villageois) in ("villageois"):
            print("Vous avez créé un", str(self.name), "de type", str(self.type))
            self.villageois = True
            self.alive = True
        else: print("Il faut choisir un type valable")

def millitaire(nb,troop,type):
    armee = {}
    for i in range (nb):
        armee[i] = Unite(troop,type)
        #creer_troop() c'est là que se fera la création réelle de troupe à mon avis
    return armee


#Peut-être rajouter une ligne pour dire combien le batiment met de temps à se construire,
#avec une classe batiments avec tous les temps de construction des batiments, et du coup faire un print(self.temps_construction_eglise) par exemple
def construire(batiment,type):
    construction = Unite(batiment,type)
    return construction


test_archers = millitaire(10,"arbalétrier","infanterie")

print(test_archers)

test_batiment = construire("hotel de ville","economie")

print(test_batiment)
