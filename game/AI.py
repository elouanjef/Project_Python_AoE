class AI:
    def __init__(self,minute,second):
        self.time = "%02d:%02d"%(minute,second)
    def read_file(self):
        f = open("action.txt","r")
        action_line = f.readline()
        action_line = action_line.rsplit("\n")
        action = action_line[0].split("-")
        return action
    def action(self):
        action = self.read_file()
        if self.time == action[0]:
            print("success")
        else:
            print("fail")


ai =AI(00,00)
ai.action()