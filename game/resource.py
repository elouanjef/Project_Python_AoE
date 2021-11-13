from .hud import *

class ResourceManager:
    def __init__(self):
        self.resources = {
            "wood" : 500,
            "rock" : 500,
            "gold" : 500,
            "food" : 500
        }
        self.costs = {
            "TownCenter": { "wood": 450, "rock": 0, "gold": 0, "food": 0 },
            "Barracks": { "wood": 125, "rock": 0, "gold": 0, "food": 0 },
            "LumberMill": {"wood": 50, "rock": 0, "gold": 0, "food": 0}
        }

    def cost_to_resource(self, building):
        for resource, cost in self.costs[building].items():
            self.resources[resource] -= cost

    def is_affordable(self, building):
        affordable = True
        for resource, cost in self.costs[building].items():
            if cost > self.resources[resource]:
                affordable = False
        return affordable
