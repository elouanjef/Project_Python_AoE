from typing import DefaultDict

from pygame.mixer import find_channel
from .events import *
from settings import *
from .buildings import *
import json

action_dict = {
    "TownCenter": 0,
    "Barracks": 1,
    "Archery": 2,
    "Archer": 3,
    "Infantryman": 4,
    "Villager": 5,
    "get_resource": 6
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
        self.AI_unit = []
        self.AI_villager = []
        self.AI_batiment = []
        with open(AI_action_JSONfile) as f:
            self.data = json.load(f)
        self.function_list = [self.AI_construct_Towncenter, self.AI_construct_Barracks, self.AI_construct_Archery,
                              self.create_Archer,self.create_Infantryman, self.create_villager, self.get_resource]
        self.towncenter = self.AI_construct_Towncenter(5,10)

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

    def AI_construct_Towncenter(self, x, y):
        # print(f'construct a Towncenter at ({x},{y})')
        if not self.world.world[x][y]["collision"]:
            ent = TownCenter((x, y), self.resource_manager, "Red", True)
            self.world.entities.append(ent)
            self.AI_batiment.append(ent)
            self.world.buildings[x][y] = ent
            self.created_tc = True
            return ent
        else: 
            if (0 < y < 49):
                return self.AI_construct_Towncenter(x, y+1)
            elif ( 0 < x < 49):
                return self.AI_construct_Towncenter(x+1, y)

    def AI_construct_Barracks(self, x, y):
        # print(f'construct a Barrack at ({x},{y})')
        if not self.world.world[x][y]["collision"]:
            ent = Barracks((x, y), self.resource_manager, "Red", False)
            self.world.entities.append(ent)
            self.AI_batiment.append(ent)
            self.world.buildings[x][y] = ent
            self.created_bar = True
        else: 
            if (0 < y < 49):
                self.AI_construct_Barracks(x, y+1)
            elif ( 0 < x < 49):
                self.AI_construct_Barracks(x+1, y)

    def AI_construct_Archery(self, x, y):
        # print(f'construct an Archery at ({x},{y})')
        if not self.world.world[x][y]["collision"]:
            ent = Archery((x, y), self.resource_manager, "Red", False)
            self.world.entities.append(ent)
            self.AI_batiment.append(ent)
            self.world.buildings[x][y] = ent
            self.created_arc = True
        else: 
            if (0 < y < 49):
                self.AI_construct_Archery(x, y+1)
            elif ( 0 < x < 49):
                self.AI_construct_Archery(x+1, y)




#================================================================================================================================================================
#=============================================================       GETTING RESSOURCE      =====================================================================
#================================================================================================================================================================



    def find_resource(self):
        vill_dict = DefaultDict(list)
        vill_list = []  # wood,rock,gold
        i = 0
        for villager in self.AI_villager:
            # print(type(villager))
            # self.world.units[self.tile["grid"][0]][self.tile["grid"][1]]
            # print(f'x:{villager.tile["grid"][0]} y:{villager.tile["grid"][1]}')
            # print(self.get_distance(villager, "Arbre"))
            # print(self.get_distance(villager, "Carrière de pierre"))
            # print(self.get_distance(villager, "Or"))
            vill_list.append(self.get_distance(villager, "Arbre"))
            vill_list.append(self.get_distance(villager, "Carrière de pierre"))
            vill_list.append(self.get_distance(villager, "Or"))
            vill_list.append(self.get_distance(villager, "Buisson"))
            vill_dict[str(i)] = vill_list
            vill_list = []
            i += 1
        return vill_dict

    def get_resource(self, resource):
        dict_resource = self.find_resource()
        if (dict_resource == {}): return

        if (resource == "Arbre"):
            min_dictance = 100  # out_of_map
            villa_pos = (-1, -1, -1)  # (x,y,keys_of_villager)
            for i in dict_resource.keys():
                if self.AI_villager[int(i)].in_work: continue  # if he/she is working, skip
                if (dict_resource[i][0][2] < min_dictance):
                    min_dictance = dict_resource[i][0][2]
                    villa_pos = (dict_resource[i][0][0], dict_resource[i][0][1], i)
            if (villa_pos == (-1, -1, -1)): return
            if self.AI_villager[int(villa_pos[2])].world.world[villa_pos[0] + 1][villa_pos[1]]["collision"]:
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # print("change Arbre 1")
                self.get_new_resource("Arbre",1)
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # print("change Arbre 2")
                self.get_new_resource("Arbre",2)
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # print("change Arbre 3")
                self.get_new_resource("Arbre",3)
                # )))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
            else:
                self.AI_villager[int(villa_pos[2])].set_target(
                    (villa_pos[0] + 1, villa_pos[1]))  # + 1 because of mining_position
                self.AI_villager[int(villa_pos[2])].in_work = True  # the villager is working
                self.world.list_mining.append(self.world.world[villa_pos[0]][villa_pos[1]])
                self.world.world[villa_pos[0]][villa_pos[1]]["mining_team"] = "Red"
                self.world.events.getting_resource() 
                self.world.mining = True


        if (resource == "Carrière de pierre"):
            min_dictance = 100  # out_of_map
            villa_pos = (-1, -1, -1)  # (x,y,keys_of_villager)
            for i in dict_resource.keys():
                if self.AI_villager[int(i)].in_work: continue
                if (dict_resource[i][1][2] < min_dictance):
                    min_dictance = dict_resource[i][1][2]
                    villa_pos = (dict_resource[i][1][0], dict_resource[i][1][1], i)
            if (villa_pos == (-1, -1, -1)): return
            if self.AI_villager[int(villa_pos[2])].world.world[villa_pos[0] + 1][villa_pos[1]]["collision"]:
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # print("change Pierre 1")
                self.get_new_resource("Carrière de pierre",1)
                # )))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
                # # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # print("change Pierre 2")
                self.get_new_resource("Carrière de pierre",2)
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # print("change Pierre 3")
                self.get_new_resource("Carrière de pierre",3)
                # )))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
                # # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # print("change Pierre 4")
                self.get_new_resource("Carrière de pierre",4)
                # )))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
            self.AI_villager[int(villa_pos[2])].set_target(
                (villa_pos[0] + 1, villa_pos[1]))  # + 1 because of mining_position
            self.AI_villager[int(villa_pos[2])].in_work = True
            self.world.list_mining.append(self.world.world[villa_pos[0]][villa_pos[1]])
            self.world.world[villa_pos[0]][villa_pos[1]]["mining_team"] = "Red"
            self.world.events.getting_resource() 
            self.world.mining = True



        if (resource == "Or"):
            min_dictance = 100  # out_of_map
            villa_pos = (-1, -1, -1)  # (x,y,keys_of_villager)
            for i in dict_resource.keys():
                if self.AI_villager[int(i)].in_work: continue
                if (dict_resource[i][2][2] < min_dictance):
                    min_dictance = dict_resource[i][2][2]
                    villa_pos = (dict_resource[i][2][0], dict_resource[i][2][1], i)
            if (villa_pos == (-1, -1, -1)): return
            if self.AI_villager[int(villa_pos[2])].world.world[villa_pos[0] + 1][villa_pos[1]]["collision"]:
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # print("change Or 1")
                self.get_new_resource("Or",1)
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # print("change Or 2")
                self.get_new_resource("Or",2)
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # print("change Or 3")
                self.get_new_resource("Or",3)
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # print("change Or 4")
                self.get_new_resource("Or",4)
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
            self.AI_villager[int(villa_pos[2])].set_target(
                (villa_pos[0] + 1, villa_pos[1]))  # + 1 because of mining_position
            self.AI_villager[int(villa_pos[2])].in_work = True
            self.world.list_mining.append(self.world.world[villa_pos[0]][villa_pos[1]])
            self.world.world[villa_pos[0]][villa_pos[1]]["mining_team"] = "Red"
            self.world.events.getting_resource() 
            self.world.mining = True


        if (resource == "Buisson"):
            min_dictance = 100  # out_of_map
            villa_pos = (-1, -1, -1)  # (x,y,keys_of_villager)
            for i in dict_resource.keys():
                if self.AI_villager[int(i)].in_work: continue
                if (dict_resource[i][3][2] < min_dictance):
                    min_dictance = dict_resource[i][3][2]
                    villa_pos = (dict_resource[i][3][0], dict_resource[i][3][1], i)
            if (villa_pos == (-1, -1, -1)): return
            if self.AI_villager[int(villa_pos[2])].world.world[villa_pos[0] + 1][villa_pos[1]]["collision"]:
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # print("change Buisson 1")
                self.get_new_resource("Buisson",1)
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # print("change Buisson 2")
                self.get_new_resource("Buisson",2)
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # print("change Buisson 3")
                self.get_new_resource("Buisson",3)
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
                # print("change Buisson 4")
                self.get_new_resource("Buisson",4)
                # ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))) 
            self.AI_villager[int(villa_pos[2])].set_target(
                (villa_pos[0] + 1, villa_pos[1]))  # + 1 because of mining_position
            self.AI_villager[int(villa_pos[2])].in_work = True
            self.world.list_mining.append(self.world.world[villa_pos[0]][villa_pos[1]])
            self.world.world[villa_pos[0]][villa_pos[1]]["mining_team"] = "Red"
            self.world.events.getting_resource() 
            self.world.mining = True



    def get_distance(self, villager, type_resource):

        distance_list = []
        for x in range(self.world.grid_size_x):
            for y in range(self.world.grid_size_y):
                if self.world.world[x][y]["tile"] == type_resource:
                    l = ((villager.tile["grid"][0] - x) ** 2 + (villager.tile["grid"][1] - y) ** 2) ** (1 / 2)
                    distance_list.append((x, y, l))
        temp_list = []
        for i in distance_list:
            temp_list.append(i[2])  # the same pos index of distance_list
        dictance_min = min(temp_list)
        return distance_list[temp_list.index(dictance_min)]

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++GETTING_NEW_RESSOURCE+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def get_new_distance(self, villager, type_resource):

        distance_list = []
        for x in range(self.world.grid_size_x):
            for y in range(self.world.grid_size_y):
                if self.world.world[x][y]["tile"] == type_resource:
                    l = ((villager.tile["grid"][0] - x) ** 2 + (villager.tile["grid"][1] - y) ** 2) ** (1 / 2)
                    distance_list.append((l, x, y))   #we do it for comparing two tuple. I must show a sorted list
        return sorted(distance_list)

    def find_new_resource(self):
        vill_dict = DefaultDict(list)
        vill_list = []  
        i = 0
        for villager in self.AI_villager:
            vill_list.append(self.get_new_distance(villager, "Arbre"))
            vill_list.append(self.get_new_distance(villager, "Carrière de pierre"))
            vill_list.append(self.get_new_distance(villager, "Or"))
            vill_list.append(self.get_new_distance(villager, "Buisson"))
            vill_dict[str(i)] = vill_list
            vill_list = []
            i += 1
        return vill_dict
            

    def get_new_resource(self, resource, i_th_time):
        dict_resource = self.find_new_resource()
        if (dict_resource == {}): return
        if (resource == "Arbre"):
            min_dictance = 100  # out_of_map
            villa_pos = (-1, -1, -1)  # (x,y,keys_of_villager)
            for i in dict_resource.keys():
                if self.AI_villager[int(i)].in_work: continue  # if he/she is working, skip
                if (dict_resource[i][0][i_th_time][0] < min_dictance):
                    min_dictance = dict_resource[i][0][i_th_time][0]
                    villa_pos = (dict_resource[i][0][i_th_time][1], dict_resource[i][0][i_th_time][2], i)
            if (villa_pos == (-1, -1, -1)): return
            if self.AI_villager[int(villa_pos[2])].world.world[villa_pos[0] + 1][villa_pos[1]]["collision"]: 
                return
            else:
                
                self.AI_villager[int(villa_pos[2])].set_target(
                    (villa_pos[0] + 1, villa_pos[1]))  # + 1 because of mining_position
                self.AI_villager[int(villa_pos[2])].in_work = True  # the villager is working
                self.world.list_mining.append(self.world.world[villa_pos[0]][villa_pos[1]])
                self.world.world[villa_pos[0]][villa_pos[1]]["mining_team"] = "Red"
                self.world.events.getting_resource() 
                self.world.mining = True
        if (resource == "Carrière de pierre"):
            min_dictance = 100  # out_of_map
            villa_pos = (-1, -1, -1)  # (x,y,keys_of_villager)
            for i in dict_resource.keys():
                if self.AI_villager[int(i)].in_work: continue  # if he/she is working, skip
                if (dict_resource[i][1][i_th_time][0] < min_dictance):
                    min_dictance = dict_resource[i][1][i_th_time][0]
                    villa_pos = (dict_resource[i][1][i_th_time][1], dict_resource[i][1][i_th_time][2], i)
            if (villa_pos == (-1, -1, -1)): return
            if self.AI_villager[int(villa_pos[2])].world.world[villa_pos[0] + 1][villa_pos[1]]["collision"]: 
                return
            else:
                
                self.AI_villager[int(villa_pos[2])].set_target(
                    (villa_pos[0] + 1, villa_pos[1]))  # + 1 because of mining_position
                self.AI_villager[int(villa_pos[2])].in_work = True  # the villager is working
                self.world.list_mining.append(self.world.world[villa_pos[0]][villa_pos[1]])
                self.world.world[villa_pos[0]][villa_pos[1]]["mining_team"] = "Red"
                self.world.events.getting_resource() 
                self.world.mining = True
        if (resource == "Or"):
            min_dictance = 100  # out_of_map
            villa_pos = (-1, -1, -1)  # (x,y,keys_of_villager)
            for i in dict_resource.keys():
                if self.AI_villager[int(i)].in_work: continue  # if he/she is working, skip
                if (dict_resource[i][2][i_th_time][0] < min_dictance):
                    min_dictance = dict_resource[i][2][i_th_time][0]
                    villa_pos = (dict_resource[i][2][i_th_time][1], dict_resource[i][2][i_th_time][2], i)
            if (villa_pos == (-1, -1, -1)): return
            if self.AI_villager[int(villa_pos[2])].world.world[villa_pos[0] + 1][villa_pos[1]]["collision"]: 
                return
            else:
                self.AI_villager[int(villa_pos[2])].set_target(
                    (villa_pos[0] + 1, villa_pos[1]))  # + 1 because of mining_position
                self.AI_villager[int(villa_pos[2])].in_work = True  # the villager is working
                self.world.list_mining.append(self.world.world[villa_pos[0]][villa_pos[1]])
                self.world.world[villa_pos[0]][villa_pos[1]]["mining_team"] = "Red"
                self.world.events.getting_resource() 
                self.world.mining = True
        if (resource == "Buisson"):
            min_dictance = 100  # out_of_map
            villa_pos = (-1, -1, -1)  # (x,y,keys_of_villager)
            for i in dict_resource.keys():
                if self.AI_villager[int(i)].in_work: continue  # if he/she is working, skip
                if (dict_resource[i][3][i_th_time][0] < min_dictance):
                    min_dictance = dict_resource[i][3][i_th_time][0]
                    villa_pos = (dict_resource[i][3][i_th_time][1], dict_resource[i][3][i_th_time][2], i)
            if (villa_pos == (-1, -1, -1)): return
            if self.AI_villager[int(villa_pos[2])].world.world[villa_pos[0] + 1][villa_pos[1]]["collision"]: 
                return
            else:
                self.AI_villager[int(villa_pos[2])].set_target(
                    (villa_pos[0] + 1, villa_pos[1]))  # + 1 because of mining_position
                self.AI_villager[int(villa_pos[2])].in_work = True  # the villager is working
                self.world.list_mining.append(self.world.world[villa_pos[0]][villa_pos[1]])
                self.world.world[villa_pos[0]][villa_pos[1]]["mining_team"] = "Red"
                self.world.events.getting_resource() 
                self.world.mining = True
        
            
#================================================================================================================================================================
#=============================================================         CREATE UNITS         =====================================================================
#================================================================================================================================================================

    def create_villager(self, pos):
        if self.created_tc:
            for i in range(-1,3):
                for j in range(-1,3):
                    if not self.world.world[self.towncenter.pos[0] + i][self.towncenter.pos[1] + j]["collision"]:
                        temp = Villager(self.world.world[self.towncenter.pos[0] + i][self.towncenter.pos[1] + j], self.world, self.resource_manager, "Red", False)
                        self.AI_villager.append(temp)
                        temp.set_target(pos)
                        return 
                # elif not self.world.world[self.towncenter.pos[0]][self.towncenter.pos[1] + 1]["collision"]:
                #     self.AI_villager.append(
                #         Villager(self.world.world[self.towncenter.pos[0]][self.towncenter.pos[1] + 1], self.world, self.resource_manager, "Red", False))
                # elif not self.world.world[self.towncenter.pos[0] + 1][self.towncenter.pos[1]]["collision"]:
                #     self.AI_villager.append(
                #         Villager(self.world.world[self.towncenter.pos[0]][self.towncenter.pos[1]], self.world, self.resource_manager, "Red", False))
    #mining ressource x = villager x - 1
    def check_villager(self):
        for i in self.AI_villager:
            if not self.world.world[i.pos[0] - 1][i.pos[1]]["collision"]:
                # print(i.in_work)
                i.in_work = False
        self.get_resource("Arbre")
        self.get_resource("Or")
        self.get_resource("Carrière de pierre")
        self.get_resource("Buisson")
                

    # create an Archer for each Archery
    def create_Archer(self,x,y):
        for i in self.world.entities:
            if i.name == "Archery" and i.team == "Red":
                a = Archer(self.world.world[i.pos[0]][i.pos[1]+1], self.world, self.world.resource_manager,
                                       "Red", False)
                self.world.list_troop.append(a)
                a.set_target((x,y))
    # Create an Infrantryman for each Barracks
    def create_Infantryman(self,x,y):
        for i in self.world.entities:
            if i.name == "Barracks" and i.team == "Red":
                a = Infantryman(self.world.world[i.pos[0]][i.pos[1]+1], self.world, self.world.resource_manager,
                                       "Red", False)
                self.world.list_troop.append(a)
                a.set_target((x,y))


#================================================================================================================================================================
#=============================================================       ATTACK AND DEFENSE     =====================================================================
#================================================================================================================================================================

    def auto_attack(self):
        pass
    def group_attacking(self):
        pass
    def auro_defense(self):
        pass

#================================================================================================================================================================
#=============================================================          ACTION OF AI        =====================================================================
#================================================================================================================================================================
    # action of AI
    def action_json(self):
        self.minute, self.second = self.game_time.get_time()
        temps = ((self.minute) * 60 + self.second) - self.previous_time
        self.time = "%02d:%02d" % (self.minute, self.second)
        if temps >= 1:
            self.previous_time = (self.minute) * 60 + self.second
            if self.world.resource_manager.starting_resources_AI["Wood"] < 50:
                self.get_resource("Arbre")
            if self.world.resource_manager.starting_resources_AI["Rock"] < 50:
                self.get_resource("Carrière de pierre")
            if self.world.resource_manager.starting_resources_AI["Gold"] < 50:
                self.get_resource("Or")
            if self.world.resource_manager.starting_resources_AI["Food"] < 50:
                self.get_resource("Buisson")
            if self.time in self.data.keys():
                i = self.data[self.time]
                for j in i:
                    action_l = list(j.keys())
                    action = action_l[0]
                    pos_l = list(j.values())
                    pos = pos_l[0].split(",")
                    pos[0], pos[1] = int(pos[0]), int(pos[1])

                    if action_dict.get(action) < 5:  # construct
                        act = self.function_list[action_dict.get(action)]
                        act(pos[0], pos[1])
                    elif action_dict.get(action) == 5:
                        act = self.function_list[action_dict.get(action)]
                        act(pos)
                    elif action_dict.get(action) == 6:
                        self.get_resource("Arbre")
                        self.get_resource("Or")
                        self.get_resource("Carrière de pierre")
                        self.get_resource("Buisson")
                    else:
                        print("U should update ur action")

            self.check_villager()

                    
#_____________________________________________________________________________________________________________________________________________________________                