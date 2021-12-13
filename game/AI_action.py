action_dict = {
    "TownCenter": 0,
    "Barracks": 1,
    "LumberMill":2
}


def AI_construct_Towcenter(x, y):
    print(f'construct a Towncenter at ({x},{y})')
def AI_construct_Barracks(x,y):
    print(f'construct a Barrack at ({x},{y})')
def AI_construct_LumberMill(x,y):
    print(f'construct a LumberMill at ({x},{y})')

function_list = [AI_construct_Towcenter,AI_construct_Barracks,AI_construct_LumberMill]