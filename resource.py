import time

class Resource:
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

chene = Resource("tree")

print(chene.tree, chene.rock)

def chop(villager):
    t = 300
    #move.to(click)
    time.sleep(t)
    #destroy_entity(entity)  pourra être géré quand on saura comment gérer les entités sur la carte tels que les arbres ou les rochers etc...

"""
def mineR(villager):

def mineG(villager):

def food(villager):
"""
