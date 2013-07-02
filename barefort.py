"""

These functions need reorganized.


Function descriptions for this file:
    Generate an empty fortress array.
    Generate a random starting coordinate on that fortress array.
    Generate a doorway or a rectangular room.
    Transpose a room.
    Print a room on the console.
    Count the percentage a total room that will be filled e.g. 20/(20*20)=5%


"""
import sys
import random

random.seed()


def fortress_array_assignment(fort_depth, fort_size):

    # The fortress_array variable is a list of list of lists.
    # The major list is z axis:  The first floor is the top list.
    # The second depth is x, and the third depth list is y
    fortress_array = []

    for z in range(0,fort_depth):
        x_direction = []
        for x in range(0,fort_size):
            y_direction = []
            for y in range(0,fort_size):
                y_direction.append("`")
            x_direction.append(y_direction)
        fortress_array.append( x_direction )
    
    return fortress_array


def initial_coords(z_max, x_max, y_max):
    """
    Choose a random starting coordinate
    """

    z_start = random.randint(0,z_max-1)
    x_start = random.randint(0,x_max-1)
    y_start = random.randint(0,y_max-1)
    
    coordinates = [z_start, x_start, y_start]

    return coordinates


def doorway_generator(coordinate):
    """
    generate a 1x1 doorway
    """

    room_array=[[["d"]]]
    
    return room_array


def rect_generator(coordinate):
    """
    generate random dimensions for a rectangular room

    the parameters should be tweaked and potentially passed.
    """
    z_axis = random.randint(1,1)
    short_axis = random.randrange(3,7,2) # step=2 makes even or odd rooms only
    long_axis = random.randrange(3,11,2) # step=2 makes even or odd rooms only
    #determine orientation
    orientation = random.randint(1,2)
    if orientation == 1:
        x_axis = short_axis
        y_axis = long_axis
    if orientation == 2:
        x_axis = long_axis
        y_axis = short_axis
    
    room_array = []

    for z in range(0,z_axis):
        x_direction = []
        for x in range(0,x_axis):
            y_direction = []
            for y in range(0,y_axis):
                y_direction.append("d")
            x_direction.append(y_direction)
        room_array.append( x_direction )

    return room_array


def transpose_room(room):
    """
    Transpose the xy plane of a room.
    
    Currently preserves the z-dimension.
    """

    room_transposed = []
    for room_xy in room: 
        room_transposed_xy = []
        length_y = len(room_xy[0])   # y-length of lol
        for t in range(0, length_y):
            transposed_y = []
            for each in room_xy:
                transposed_y.append(each[t])
            room_transposed_xy.append(transposed_y)
        room_transposed.append(room_transposed_xy)
    
    return room_transposed


def print_fort(fortress_array):

    for z in fortress_array:
        for x in z:
            print_string = ""
            for y in x:
                print_string += y 
            print print_string
        print "\n"


def enumerate_dig_area(fortress_array):

    total_blocks = 0
    empty_blocks = 0
    for z in fortress_array:
        for x in z:
            for y in x:
                total_blocks += 1
                if y == "`":
                    empty_blocks += 1

    return [empty_blocks, total_blocks]


