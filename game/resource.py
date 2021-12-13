from .gui import *


class Resource:
    def __init__(self):
        self.starting_resources = {
            "wood": 5000,
            "rock": 500,
            "gold": 500,
            "food": 500
        }
        self.costs = {
            "TownCenter": {"wood": 450, "rock": 0, "gold": 0, "food": 0},
            "Barracks": {"wood": 125, "rock": 0, "gold": 0, "food": 0},
            "LumberMill": {"wood": 50, "rock": 0, "gold": 0, "food": 0},
            "Archery": {"wood": 125, "rock": 0, "gold": 0, "food": 0},
            "Archer": {"wood": 0, "rock": 0, "gold": 0, "food": 20},
            "Infantryman": {"wood": 0, "rock": 0, "gold": 0, "food": 30},
            "Villager": {"wood": 0, "rock": 0, "gold": 0, "food": 50}
        }

    def cost_to_resource(self, building):
        for resource, cost in self.costs[building].items():
            self.starting_resources[resource] -= cost

    def is_affordable(self, building):
        affordable = True
        for resource, cost in self.costs[building].items():
            if cost > self.starting_resources[resource]:
                affordable = False
        return affordable


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
