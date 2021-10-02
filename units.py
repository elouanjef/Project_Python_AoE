from typing import Dict

class attTroop:

    archer_time = 3
    archer_resWRGF = [20,20,20,30]

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

def attributs(nom,resWRGF):  # Cette fonction servira a retourner les informations sur la troupe ou le batiment pour ainsi dire :
                                # elle met tant de temps à se construire, elle coute tant de bois etc...
    costw = resWRGF[0]
    costr = resWRGF[1]
    costg = resWRGF[2]
    costf = resWRGF[3]
    if nom in ("arbalétrier"):
        print("Un(e)",nom, "vaut :", costw, "bois", costr, "pierre", costg, "or", costf, "nourriture\nElle met",attTroop.archer_time,"secondes à se créer.")
    elif nom.batiment:
        print("Un(e)",nom, "vaut :", costw, "bois", costr, "pierre", costg, "or", costf, "nourriture")
    elif nom.villageois:
        print("Un(e)",nom, "vaut :", costw, "bois", costr, "pierre", costg, "or", costf, "nourriture")


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

print(str(test_archers[5]))
print(attributs((test_archers[5].name),attTroop.archer_resWRGF))


#test_batiment = construire("hotel de ville","economie")
#print(test_batiment)



#c'est un exemple, j'ai pas tout terminé, la fonction attribut n'est pas du tout au point
