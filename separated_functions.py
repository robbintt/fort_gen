"""
The goal is to display data, e.g. d,i,j,u,` in an indexed format.

The array this data is stored in can expand in both the negative
and positive directions on the x, y, and z axis.

There is no disadvantage each room node onto a table, and then when
generating the next node, check for collisions.

Process:
    Generate next node type
    Determine starting point in the array
    Assess overlap with any previously written node.
    In order to do this, all nodes should be buffered by
    the tilde character that means 'do nothing' for quickfort

"""
import sys
import random
import csv

import barefort

random.seed()

# does nothing yet, do not change
fort_depth=1

# fort size is defined by one variable which determines xy array size.
fort_size=30

# determines maximum depth of recursive branching algorithm.
# intrinsically limits the fort size to max of node_depth^node depth rooms.
node_depth=20

#percent required to be dug out
perc_dug_out=15

def room_generator(coordinate, fortress_array, room_type="rect"):
    """
    use an algorithm to select a function, potentially randomization
    default to rect for now
    """

    # the generated room should be a list of list of lists
    # and mirror the format of fortress array
    generated_room = []

    if room_type == "rect":
        generated_room = barefort.rect_generator(coordinate)
    elif room_type == "doorway":
        generated_room = barefort.doorway_generator(coordinate)
    else:
        generated_room = barefort.rect_generator(coordinate)
   
    return generated_room


def perimeter_define():
    """
    Define a room perimeter. One use is to randomly select doorway location.
    """
    pass
    

def rect_collision_detector(coordinate, fortress_array, generated_room):
    """
    This takes a generated_room and a coordinate, and detects if it will 
    collide with the edge of the fortress_array
    """
    
    # This represents the size of the room on all three (z,x,y) axes
    z_size = len(generated_room)
    x_size = len(generated_room[0])
    y_size = len(generated_room[0][0])
    
    # This is the theoretical end of the generated room.
    z_end = z_size + int(coordinate[0])  
    x_end = x_size + int(coordinate[1]) 
    y_end = y_size + int(coordinate[2]) 

    # This is the total length of the fortress.
    z_fort_total_len = len(fortress_array)
    x_fort_total_len = len(fortress_array[0])
    y_fort_total_len = len(fortress_array[0][0])

    # check that coordinates+size doesn't overflow the fortress_array.
    # if it does, we could test the opposite direction on fortress_array
    repeat_flag = 0

    if z_end > z_fort_total_len:
        repeat_flag = 1
    if x_end > x_fort_total_len:
        repeat_flag = 1
    if y_end > y_fort_total_len:
        repeat_flag = 1
    
    if repeat_flag == 1:
        return 1
    else:
        return 0

    # Catch any crazy case where the if/else were to fail.
    return 0


def room_collision_detector(coordinate, fortress_array, generated_room):
    """ detect collision with any other "d" on the fortress_array
     if colission is found, set a new coordinate according to the symmetry
     parameters of the room size.  If a collision remains, try transposing
     the room. If this doesn't do enough, abort the node. """
    
    
    # This represents the size of the room on all three (z,x,y) axes
    z_size = len(generated_room)
    x_size = len(generated_room[0])
    y_size = len(generated_room[0][0])

    for z_dig in range(0,z_size):
        for x_dig in range(0,x_size):
            for y_dig in range (0,y_size):

                # define the absolute position for the iterated coordinate
                z_abs = z_dig+coordinate[0]
                x_abs = x_dig+coordinate[1]
                y_abs = y_dig+coordinate[2]

                if fortress_array[z_abs][x_abs][y_abs] != "`":
                    return 1
    
    return 0


def transform_coordinate(x, coordinate, x_size, y_size):
    """ 
    Transform a coordinate on two axes given x randomly iterates through 
    range(0,3) until a match is found.
    """

    #Catch any size < 2 transformations.
    if x_size < 2 or y_size < 2:
        return coordinate

    # Add 1 to x_size and y_size to ensure that the originating block is still
    # part of the transformed block.

    if x == 0:
        return coordinate
    if x == 1:
        if coordinate[1]-x_size+1 < 0:
            return coordinate
        else:
            return [coordinate[0],coordinate[1]-x_size+1,coordinate[2]]
    if x == 2:
        if coordinate[2]-y_size+1 < 0:
            return coordinate
        else:
            return [coordinate[0],coordinate[1],coordinate[2]-y_size+1]
    if x == 3:
        if coordinate[2]-y_size+1 < 0 or coordinate[1]-x_size+1 < 0:
            return coordinate
        else:
            return [coordinate[0],coordinate[1]-x_size+1,coordinate[2]-y_size+1]

    # Error case:
    return coordinate


def room_installer(coordinate, fortress_array, generated_room):
    """
    Defining the room geometry
    Each point in generated_room must be transcribed to fortress_array
    """
    
    # This represents the size of the room on all three (z,x,y) axes
    z_size = len(generated_room)
    x_size = len(generated_room[0])
    y_size = len(generated_room[0][0])

    # This is the total length of the fortress.
    z_fort_total_len = len(fortress_array)
    x_fort_total_len = len(fortress_array[0])
    y_fort_total_len = len(fortress_array[0][0]) 
    
    # return collision with the edge of fortress_array.
        # try flipping the map on the x axis, and then the y axis,
        #   and then both.
        # So if the map were considered the LRQ, of the graph,
        #   we would try the LLQ, ULQ, and URQ.
        # This is done by moving the coordinates by the x and y length of
        #   the room.
    rect_direction = range(0,3)
    random.shuffle(rect_direction)
   

    # Randomly transform the room inherently.
    for x in rect_direction:
        test_trans_coordinate = transform_coordinate(x, coordinate, x_size, y_size)
        if rect_collision_detector(test_trans_coordinate, fortress_array, generated_room) == 0:
            coordinate = test_trans_coordinate
            break
        else:
            return 2  ## For loop fails to find non-colliding room.
        return 2 # just a catch all, should never be hit.

        
    # return collision with another room.
    if room_collision_detector(coordinate, fortress_array, generated_room) == 1:
        return 2
    
    """ place the room and detect the perimeter """
    candidate_coordinates = []  # store random coordinate candidates
    for z_dig in range(0,z_size):
        for x_dig in range(0,x_size):
            for y_dig in range(0,y_size):

                # define the absolute position for the iterated coordinate
                z_abs = z_dig+coordinate[0]
                x_abs = x_dig+coordinate[1]
                y_abs = y_dig+coordinate[2]
                
                # If the random coordinate is a perimeter coordinate, save
                #     in the candidate_coordinates list.
                #
                # The additional arguments in each if statement avoids
                #     all corners.
                #
                if x_dig == 0:
                    if x_abs-1 >= 0:
                        candidate_coordinates.append([z_abs, x_abs-1, y_abs])
                if x_dig == x_size-1:
                    if x_abs+1 <= x_fort_total_len-1:
                        candidate_coordinates.append([z_abs, x_abs+1, y_abs])
                if y_dig == 0:
                    if y_abs-1 >= 0:
                        candidate_coordinates.append([z_abs, x_abs, y_abs-1])
                if y_dig == y_size-1:
                    if y_abs+1 <= y_fort_total_len-1:
                        candidate_coordinates.append([z_abs, x_abs, y_abs+1])
                
                # place the dig notation for each space
                fortress_array[z_abs][x_abs][y_abs] = "d"
    
    # select a coordinate for the next room.
    
    next_coord = next_coordinate(candidate_coordinates, fortress_array)
    
    return [fortress_array, next_coord]


def next_coordinate(candidate_coordinates, fortress_array):
    """
    select the next coordinate from a list of candidate_coordinates.

    rank each coordinate by the number of neighbors with ` in their space.
    
    If the coordinate is empty, add 100.

    For each cardinal or diagonal neighbor empty, add 10.
        
    The highest rank wins.
    """

    coord_score_pair = [] # list of pairs of coordinates and rank
    for each in candidate_coordinates:
        score = 0
        # print "New Test:", each
        for z in range(-1,2):
            for x in range(-1,2):
                for y in range(-1,2):
                    
                    # Break out if any absolute coordinate is < 0
                    # This will prevent the negative value from wrapping
                    # to the other side of the map.
                    if each[0]+z < 0:
                        break
                    if each[1]+x < 0:
                        break
                    if each[2]+y < 0:
                        break


                    #try:
                    #    print "[z,x,y]", z,x,y
                    #    print "Current exact location:", each[0]+z,each[1]+x,each[2]+y
                    #    print "Current check is:", fortress_array[each[0]+z][each[1]+x][each[2]+y]
                    #except:
                    #    pass
                    if z == 0 and x == 0 and y == 0:
                        try:
                            if fortress_array[each[0]+z][each[1]+x][each[2]+y] == "`":
                                score += 100
                        except:
                            pass
                    else:
                        try:
                            if fortress_array[each[0]+z][each[1]+x][each[2]+y] == "`":
                                score += 10
                        except:
                            pass

        
        each_and_score = [each, score]
        coord_score_pair.append(each_and_score)
    
    # Sort the possible scores so top scores are at the *end*.
    coord_score_pair.sort(key=lambda x: x[1])
    
    # Assign top score from the last item in coord_score_pair
    top_score = coord_score_pair[-1][1]
    
    # Check each for top score status and add to a list of equal top scores.
    randomize_top_score = []
    for each in coord_score_pair:
        if each[1] == top_score:
            randomize_top_score.append(each)

    # Assign a new random coordinate from the list of top scores.
    new_random_top_coordinates = randomize_top_score[random.randint(0,len(randomize_top_score)-1)][0]

    #waiting_func = raw_input("Press Enter to continue...")

    return new_random_top_coordinates ## for now


def depth_iterator(coordinate, fortress_array, node_depth=5):
    """
    Recursively generate deeper nodes, check them for collisions, resize
    them if necessary, and write them to the fortress_array.


    """
    if node_depth <= 0:
        return fortress_array # stop here
    node_depth -= 1
    #print "Depth test:", node_depth
  
    # This is a negative feedback loop, making a branch more probable
    # each time the node depth goes down.
    if random.randint(1,3*(node_depth+1)) == 1:
        depth_iterator(coordinate, fortress_array, node_depth)

    roomtype_randomizer = random.randint(1,3)
    if roomtype_randomizer < 3:
        next_room = room_generator(coordinate, fortress_array, "doorway")
    else:
        next_room = room_generator(coordinate, fortress_array, "rect")

    test_array = room_installer(coordinate, fortress_array, next_room)
    
    #if room installer fails, generate another attempt.
    if test_array == 1:
        # use the depth iterator to find a good room node_depth times.
        # the traversal limit doesn't affect the parent function limits.
        test_array = [fortress_array, coordinate]
    elif test_array == 2:
        # if the room installer totally fails
        test_array = [fortress_array, coordinate]
    else:
        pass
    
    fortress_array = test_array[0]
    next_coordinates = test_array[1]

    # Recurse on the new results!
    # But how will I track what kind of room to do next?
    depth_iterator(next_coordinates, fortress_array, node_depth)

    return [fortress_array, next_coordinates]

