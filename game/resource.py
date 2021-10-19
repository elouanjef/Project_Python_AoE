from .hud import *

class Resource:
    def __init__(self, wood, rock, gold, food):
        self.gold = gold
        self.rock = rock
        self.wood = wood
        self.food = food

    def get_res(self):
        return [self.wood, self.rock, self.gold, self.food]

    #def consume(self, res):
