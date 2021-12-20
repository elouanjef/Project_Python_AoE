from .gui import *


class Resource:
    def __init__(self):
        self.starting_resources = {
            "Wood": 2000,
            "Rock": 500,
            "Gold": 500,
            "Food": 500
        }
        self.starting_resources_AI = {
            "Wood": 2000,
            "Rock": 500,
            "Gold": 500,
            "Food": 500
        }
        self.costs = {
            "TownCenter": {"Wood": 450, "Rock": 0, "Gold": 0, "Food": 0},
            "Barracks": {"Wood": 125, "Rock": 0, "Gold": 0, "Food": 0},
            "LumberMill": {"Wood": 50, "Rock": 0, "Gold": 0, "Food": 0},
            "Archery": {"Wood": 125, "Rock": 0, "Gold": 0, "Food": 0},
            "Archer": {"Wood": 0, "Rock": 0, "Gold": 0, "Food": 20},
            "Infantryman": {"Wood": 0, "Rock": 0, "Gold": 0, "Food": 30},
            "Villager": {"Wood": 0, "Rock": 0, "Gold": 0, "Food": 50}
        }

    def is_affordable(self, ent):
        affordable = True
        for resource, cost in self.costs[ent].items():
            if cost > self.starting_resources[resource]:
                affordable = False
        return affordable

    def buy(self, ent):
        # print(ent.name)
        if ent.team == "Blue":
            for resource, cost in self.costs[ent.name].items():
                self.starting_resources[resource] -= cost
        elif ent.team == "Red":
            for resource, cost in self.costs[ent.name].items():
                if self.starting_resources_AI[resource] > cost:
                    self.starting_resources_AI[resource] -= cost
                else:
                    print("not enough ressource!!!!")


"""class Resource:
    tree = False
    rock = False
    gold = False
    bush = False
    animal = False

    def __init__(self,type):
        self.type = type
        if str(self.type) == 'tree': self.tree = True
        elif str(self.type) == 'rock': self.rock = True
        elif str(self.type) == 'gold': self.gold = True
        elif str(self.type) == 'bush': self.bush = True
        elif str(self.type) == 'animal': self.animal = True
        else : print('Type de ressource non valable.')

def chop(villager):
    t = 300
    #move.to(click)
    time.sleep(t)
    #destroy_entity(entity)  pourra être géré quand on saura comment gérer les entités sur la carte tels que les arbres ou les rochers etc...

"""
