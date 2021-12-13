from .AI_action import *
from .events import *
from settings import *


class AI:
    def __init__(self,game_time):
        self.game_time = game_time
        self.previous_time = 0
        self.f = open(AI_action_file,"r")
    def read_file(self):
        action_line = self.f.readline()
        action_line = action_line.rsplit("\n")
        action = action_line[0].split("-")
        return action
    def action(self):
        self.minute,self.second = self.game_time.get_time()
        temps = ((self.minute)*60 + self.second) - self.previous_time
        self.time = "%02d:%02d"%(self.minute,self.second)
        if temps >= 1:
            self.previous_time = (self.minute)*60 + self.second
            action = self.read_file()
            print(self.time)
            if self.time == action[0]:   #Nécessité d'utiliser une approximation car le timing est difficile à être précis
                if action[1] in action_dict.keys():
                    act = function_list[action_dict.get(action[1])]
                    act(5,10)
                else:
                    pass 


