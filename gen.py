import covid_stack as stk
from PIL import Image

def people_gen(population):
    """Makes virtual representations of people. Medically trained professional not required, although highly recommended."""
    for i in range(population):
        person = stk.person()
        stk.people.append(person)
def represent():
    """Represents current stk.environment in terms of the textual representation of the type of the
     areas that make it up."""
    represent = []
    types = {}
    for i in stk.environment:
        temp = []
        for i2 in i:
            temp.append(i2.type)
            if i2.type not in types:
                types[i2.type] = 1
            else:
                types[i2.type] += 1
        represent.append(temp)
    print(represent)
    print(types)
    return represent, types

def represent_as_image(environ):
    """Represents current passed environment as one image for each floor. Works for a 3d array. 
    Won't work for detailed stk.environment until rooms are created in detail"""
    t = False
    if type(environ) == stk.area:
        t = True
    for floor_num in range(len(environ)):
        img = Image.new("RGB",(len(environ[floor_num]), len(environ[floor_num][0])))
        for l in range(len(environ[floor_num])):
            for w in range(len(environ[floor_num][l])):
                if t == False:
                    img.putpixel((l,w), stk.colors[environ[floor_num][l][w]])
                else:
                    img.putpixel((l,w), stk.colors[environ[floor_num][l][w].type])
        img = img.resize((len(environ[floor_num])*100, len(environ[floor_num][0])*100),resample=Image.NEAREST)
        img.save("floor " + str(floor_num) + ".jpg")



    

def unpack(floors, parameters):
    """Unpacks the kwargs value (stored in parameters) into a dictionary with each building type keyed to 
    its value per floor and remainder to be distributed. If only the TSA was this fast."""
    final = {}
    for key, value in parameters.items():
        per_floor = int(value/floors)
        final[key] = [per_floor, value%floors]
    return final
def assign_environs(values, which):
    """Evenly distributes all room types, with the remainders put on a soon to be defunct top floor."""
    temp = []
    for key, value in values.items():
        for i in range(value[which]):
            temp.append(key)
    for i in range(len(temp)):
        temp[i] = stk.area(temp[i], stk.params[temp[i]])
    stk.environment.append(temp)
def low_detail_assign(floors, parameters):
    """Assigns lower detail environments. Additionally, redistributes top floor of remainders then deletes it.
     With these, transmission while on the move is not examined."""
    values = unpack(floors, parameters)
    for i in range(floors):
        assign_environs(values, 0)
    assign_environs(values, 1)
    if stk.environment[-1] == []:
        del stk.environment[-1]
    if len(stk.environment) > floors:
        types = {}
        for i in stk.environment[-1]:
            if i.type not in types:
                types[i.type] = [i.type]
            else:
                types[i.type].append(i.type)
        del stk.environment[-1]
        for value in types.values():
            enum = 0
            for i in value:
                val = stk.area(i, stk.params[i])
                stk.environment[enum].append(val)
                enum += 1

def border_create(total):
    """ Creates borders given total area. Borders are optimized to be as square as possible. Additional area is added
    to make room for required environmental features (hallways, closets, etc.)"""
    diff, quotient, dividend = [], [], []
    for i in range(1,total):
        dividend.append(i)
        quotient.append(total/i)
        diff.append(abs(i - (total/i)))
    factors = [dividend[diff.index(min(diff))], quotient[diff.index(min(diff))]]
    finished = []
    for i in factors:
        if i != int(i):
            finished.append(int(i+3))
        else:
            finished.append(int(i+4))
    return finished[0], finished[1]
        
def base_model_creation():
    model_areas = []
    for i in stk.environment:
            temp = []
            total = 0
            for i2 in i:
                temp.append(i2.size)
                total = total + i2.size
            temp.append(total)
            model_areas.append(temp)
    model_dimensions = []
    for i in range(len(model_areas)):
            total = model_areas[i].pop()
            l,w = border_create(total)
            model_dimensions.append([l,w])
    temp_model = []
    for floor in model_dimensions:
            l, w = floor[0], floor[1]
            temp_floor = []
            for horiz_line in range(l):
                temp = []
                for space in range(w):
                    temp.append("un")
                temp_floor.append(temp)
            temp_model.append(temp_floor)
    return temp_model

def hallway_maker(environment):
    """Makes hallways. Pretty self explanatory. Just pass an array"""
    for floor in environment:
        width = len(floor) #iterate horizontally 
        length = len(floor[0]) #iterate down 
        if width >= 40:
            hallways_num = int(width/40)
            hallways_width = int(width/(hallways_num+1))
        else:
            hallways_num = 1
            hallways_width = int(width/2)
        if length >= 20:
            hallways2_num = int(length/20)
            hallways2_width = int(length/(hallways2_num+1))
        else:
            hallways2_num = 1
            hallways2_width  = int(length/2)
        for position in range(len(floor)):
            if position%hallways_width == 0 and position != 0 and position != len(floor) - 1:
                for loc in range(len(floor[position])):
                    floor[position][loc] = "h" #assigns to hallway
            for loc in range(len(floor[position])):
                if loc%hallways2_width == 0 and loc != 0 and loc != len(floor[position]) - 1:
                    floor[position][loc] = "h"
    return environment

#python arrays decrease in complexity. if 3d, [z][y][x], if 2d, [y][x]

def start_finder(environment, floor_num):
    """Finds the place to start, building outward from the intersection between two hallways"""
    floor = environment[floor_num]
    horiz_hallways_loc = []
    for ypos in range(len(floor)):
        for xpos in range(1):
            if floor[ypos][xpos] == "h":
                horiz_hallways_loc.append(ypos)
    positions = []
    for y_loc_pos in range(len(horiz_hallways_loc)):
        y_loc = horiz_hallways_loc[y_loc_pos]
        for x_loc in range(len(floor[y_loc])):
            if y_loc_pos == len(horiz_hallways_loc) - 1:
                if floor[y_loc+1][x_loc] == "h":
                    positions.append([[y_loc+1, x_loc+1], [1,1]]) #y,x
                    positions.append([[y_loc+1, x_loc-1], [1,-1]]) #y,x
                if floor[y_loc-1][x_loc] == "h":
                    positions.append([[y_loc-1, x_loc+1], [-1,1]]) #y,x
                    positions.append([[y_loc-1, x_loc-1], [-1,-1]]) #y,x
            else:
                if floor[y_loc+1][x_loc] == "h":
                    positions.append([[y_loc+1, x_loc+1], [1,1]]) #y,x
                    positions.append([[y_loc+1, x_loc-1], [1,-1]]) #y,x
    return positions

def assigner(floor, position, assigned, vector, current_size, max_size, start):
    """Accepts current position, type of room to assign, direction to move, max size of room, current size of room. 
    Recursive function. Creates room in vector y direction until border reached. If created room is only one wide, 
    cut in half and put it in next row in vector x direction. If it reaches the end and there are still locations left over, 
    move back to start and iterate in vector x direction"""
    y_pos = position[0]
    x_pos = position[1]
    while current_size < max_size:
        try:
            if floor[x_pos][y_pos] == "un":
                floor[x_pos][y_pos] = assigned
                current_size += 1 
            assigner(floor, [y_pos + vector[0], x_pos], assigned, vector, current_size, max_size)
        except IndexError:
            assigner(floor, [start[0], x_pos + vector[1]], assigned, vector, current_size, max_size)
    return [floor, [y_pos, x_pos]]
            
def check_size(floor, start, vector):
    """Checks size given a 2d floor, a start position, and a vector to iterate with."""
    max = []
    y_pos = start[0]
    x_pos = start[1]
    try:
        while True:
            y_pos += vector[0]
            if floor[y_pos][x_pos] == "h":
                max[0] = y_pos
                break
    except IndexError:
        max[0] = y_pos
    try:
        while True:
            x_pos += vector[1]
            if floor[y_pos][x_pos] == "h":
                max[1] = x_pos
                break
    except IndexError:
        max[1] = x_pos
    return max[0]*max[1]

def placer(floor_num, environment, template, positions):
    """Places rooms in floor. Given the number floor to place in, the environment containing the floor, 
    a template of available rooms, and a start position"""
    floor = environment[floor_num]
    available = template[floor_num]
    for pos_base in positions:
        now_pos = pos_base
        room_area_size = check_size(floor,  now_pos[0], now_pos[1])
        for room in available:
            available.remove(room)
            temp = assigner(floor, now_pos[0], room, now_pos[1], 0, stk.params[room], now_pos[0])
            floor = temp[0]
            now_pos = [temp[1], now_pos[1]]

def enviro_gen(low_detail,floors, **parameters):
    """Generates environment"""
    low_detail_assign(floors, parameters)
    if low_detail == False:
        model_low_detail = represent()[0]
        temp_model = base_model_creation()
        temp_model = hallway_maker(temp_model)
        represent_as_image(temp_model)
        print(temp_model)
        for floor_num in range(len(temp_model)): #now assigning rooms into floors
            start_positions = start_finder(temp_model, floor_num)
            placer(floor_num, temp_model, model_low_detail, start_positions)
            



  

enviro_gen(False, 6, b1 = 5, s1 = 13, s3 = 9)