from typing import Dict


class Unit:

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
        assert self.type in ("cavalerie","infanterie","artillerie"), self.type
        print("Vous avez enrôlé un(e)",str(self.name,"de type",str(self.type)))
        Unit.alive = True

    def stats(self,costw,costf,costg,costr):
        self.costw = costw
        self.costf = costf
        self.costg = costg
        self.costr = costr

class Batiment:

    alive = True
    type = False
    name = False
    costw = 0
    costf = 0
    costg = 0
    costr = 0

    def __init__(self, name, type):
        self.name = name
        self.type = type
        assert self.type in ("militaire", "economie"), self.type
        print("Vous avez bâti un(e)",str(self.name),"de type",str(self.type))
        Batiment.alive = True

    def stats(self,costw,costf,costg,costr):
        self.costw = costw
        self.costf = costf
        self.costg = costg
        self.costr = costr

class Unite:

    batiment = False
    soldat = False
    alive = False
    type = False
    name = False
    costw = 0
    costf = 0
    costg = 0
    costr = 0

    def stats(self,costw,costr,costg,costf):
        self.costw = costw
        self.costr = costr
        self.costg = costg
        self.costf = costf
        if self.soldat:
            print("Unité ajoutée !",str(self.name),"vaut :",costw,"bois",costr,"pierre",costg,"or",costf,"nourriture")
        else: print("Bâtiment ajouté !",str(self.name),"vaut :",costw,"bois",costr,"pierre",costg,"or",costf,"nourriture")

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
        else: print("Il faut choisir un type valable")


