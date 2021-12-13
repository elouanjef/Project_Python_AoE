def read_file():
    f = open("AI_action_test.txt","r")
    action_line = f.readline()
    if (action_line == ''):
        action_line = ' - '
    action_line = action_line.rsplit("\n")
    action = action_line[0].split("-")
    li = action[2][1:-1].split(',')
    li = (int(li[0]),int(li[1]))
    action[2] = li
    return action


print(read_file())
