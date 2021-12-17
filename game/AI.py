from .events import *
from settings import *
from .buildings import *
import json

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
        self.created_tc = False
        self.created_bar = False
        self.created_arc = False
        with open(AI_action_JSONfile) as f:
            self.data = json.load(f)
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
        if not self.world.world[x][y]["collision"]:
            ent = TownCenter((x, y), self.resource_manager, "Red")
            self.world.entities.append(ent)
            self.world.buildings[x][y] = ent
            self.created_tc = True
        # else: print("peux pas construire")

    def AI_construct_Barracks(self, x, y):
        #print(f'construct a Barrack at ({x},{y})')
        if not self.world.world[x][y]["collision"]:
            ent = Barracks((x, y), self.resource_manager, "Red")
            self.world.entities.append(ent)
            self.world.buildings[x][y] = ent
            self.created_bar = True
        # else: print("peux pas construire")


    def AI_construct_Archery(self, x, y):
        #print(f'construct an Archery at ({x},{y})')
        if not self.world.world[x][y]["collision"]:
            ent = Archery((x, y), self.resource_manager, "Red")
            self.world.entities.append(ent)
            self.world.buildings[x][y] = ent
            self.created_arc = True
        # else: print("peux pas construire")


    def create_villager(self,pos):
        if self.created_tc:
            Villager(self.world.world[pos[0]][pos[1]], self.world, self.resource_manager, "Red")

    def action_json(self):
        self.minute, self.second = self.game_time.get_time()
        temps = ((self.minute) * 60 + self.second) - self.previous_time
        self.time = "%02d:%02d" % (self.minute, self.second)
        if temps >= 1:
            self.previous_time = (self.minute) * 60 + self.second
            #print(f"{self.time}")
            # if self.time in self.data.keys():
            #     for i in self.data.values():
            #         for j in i:
            #             action_l = list(j.keys())
            #             action= action_l[0]
            #             pos_l = list(j.values())
            #             pos = pos_l[0].split(",")
            #             pos[0], pos[1] = int(pos[0]), int(pos[1])
            #             print(f'pos   {pos}')

            #             if action_dict.get(action) < 3:  #construct
            #                 act = self.function_list[action_dict.get(action)]
            #                 act(pos[0], pos[1])
            #             elif action_dict.get(action) == 3:
            #                 act = self.function_list[action_dict.get(action)]
            #                 act(pos)
            if self.time in self.data.keys():
                i = self.data[self.time]
                #print(i)
                for j in i:
                    action_l = list(j.keys())
                    action= action_l[0]
                    pos_l = list(j.values())
                    pos = pos_l[0].split(",")
                    pos[0], pos[1] = int(pos[0]), int(pos[1])

                    if action_dict.get(action) < 3:  #construct
                        act = self.function_list[action_dict.get(action)]
                        act(pos[0], pos[1])
                    elif action_dict.get(action) == 3:
                        act = self.function_list[action_dict.get(action)]
                        act(pos)

                   
