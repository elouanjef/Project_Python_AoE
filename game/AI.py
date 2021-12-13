from .events import *
from settings import *
from .buildings import *

action_dict = {
    "TownCenter": 0,
    "Barracks": 1,
    "Archery": 2,
    "Villager": 3
}


class AI:
    def __init__(self, game_time, world, resource_manager):
        self.game_time = game_time
        self.world = world
        self.resource_manager = resource_manager
        self.previous_time = 0
        self.f = open(AI_action_file, "r")
        self.function_list = [self.AI_construct_Towcenter, self.AI_construct_Barracks, self.AI_construct_Archery,self.create_villager]

    def read_file(self):
        action_line = self.f.readline()
        if (action_line == ''):
            action_line = ' - -(0,0)'
        action_line = action_line.rsplit("\n")
        action = action_line[0].split("-")
        li = action[2][1:-1].split(',')
        li = (int(li[0]), int(li[1]))
        action[2] = li
        return action

    def AI_construct_Towcenter(self, x, y):
        #print(f'construct a Towncenter at ({x},{y})')
        ent = TownCenter((x, y), self.resource_manager, "Red")
        self.world.entities.append(ent)
        self.world.buildings[x][y] = ent

    def AI_construct_Barracks(self, x, y):
        #print(f'construct a Barrack at ({x},{y})')
        ent = Barracks((x, y), self.resource_manager, "Red")
        self.world.entities.append(ent)
        self.world.buildings[x][y] = ent

    def AI_construct_Archery(self, x, y):
        #print(f'construct an Archery at ({x},{y})')
        ent = Archery((x, y), self.resource_manager, "Red")
        self.world.entities.append(ent)
        self.world.buildings[x][y] = ent

    def create_villager(self,action):
        Villager(self.world.world[action[2][0]][action[2][1]], self.world, self.resource_manager)

    def action(self):
        self.minute, self.second = self.game_time.get_time()
        temps = ((self.minute) * 60 + self.second) - self.previous_time
        self.time = "%02d:%02d" % (self.minute, self.second)
        if temps >= 1:
            self.previous_time = (self.minute) * 60 + self.second
            action = self.read_file()
            # print(self.time)
            # print(f'action: {action} action[0]: {action[0]} action[1]: {action[1]}')
            # print(self.time == action[0])
            # print(type(self.time))
            # print("------------------------------------------------")
            if self.time == action[0]:  # Nécessité d'utiliser une approximation car le timing est difficile à être précis
                if action[1] in action_dict.keys():
                    if action_dict.get(action[1]) < 3:  #construct
                        act = self.function_list[action_dict.get(action[1])]
                        act(action[2][0],action[2][1])
                    elif action_dict.get(action[1]) == 3:
                        try:
                            act = self.function_list[action_dict.get(action[1])]
                            act(action)
                        except IndexError:
                            print(action_dict.get(action[1]))
                        #Villager(self.world.world[action[2][0]][action[2][1]], self.world, self.resource_manager)
                else:
                    pass 
                for i in self.world.entities:
                    print(f'{i.game_name}')
