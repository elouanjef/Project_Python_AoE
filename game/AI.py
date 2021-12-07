action_dict = {
    "TownCenter": 0,
    "Barracks": 1,
    "LumberMill":2
}

function_list = []


class AI:
    def __init__(self,minute,second):
        self.time = "%02d:%02d"%(minute,second)
    def read_file(self):
        f = open("action.txt","r")
        action_line = f.readline()
        action_line = action_line.rsplit("\n")
        action = action_line[0].split("-")
        return action
    # def action(self):
    #     action = self.read_file()
    #     if self.time == action[0]:
    #         print("success")
    #     else:
    #         print("fail")
    def action(self, game_time):
        action = self.read_file()
        if self.time == action[0]:
            if action[1] in action_dict.keys():
                act = function_list[action_dict.get(action[1])] 