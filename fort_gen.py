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
import separated_functions

random.seed()

# does nothing yet, do not change
fort_depth=1

# fort size is defined by one variable which determines xy array size.
fort_size=20

# determines maximum depth of recursive branching algorithm.
# intrinsically limits the fort size to max of node_depth^node depth rooms.
node_depth=30

#percent required to be dug out
perc_dug_out=30


def initiate(fort_depth, fort_size, node_depth):
    
    # initiate empty fortress
    fortress_array = barefort.fortress_array_assignment(fort_depth, fort_size)
    
    # initiate random starting coordinate
    coordinate = barefort.initial_coords(fort_depth, fort_size, fort_size)
    
    #print coordinate
    
    # pass fortress_array and coordinate to the depth_iterator to make nodes
    # upon completion of the depth_iterator, write the new fortress_array
    depth_iterator_array = separated_functions.depth_iterator(coordinate, fortress_array, node_depth)
    
    fortress_array = depth_iterator_array[0]

    enum_perc = barefort.enumerate_dig_area(fortress_array)
    perc_dug_out =  100 * (enum_perc[1]-enum_perc[0]) / enum_perc[1]

    return [fortress_array, perc_dug_out]


def brute_force_selector(perc_dug_out, fort_depth, fort_size, node_depth):
    """ 
    Select a high percentage map by brute forcing across the space.
    """
    multi_floor_selection = []
    for x in range(0,10000):
        print x, "of 10,000 attempts complete."
        result_attempt = initiate(fort_depth, fort_size, node_depth)
        if result_attempt[1] > perc_dug_out:
            
            
            barefort.print_fort(result_attempt[0])
            print result_attempt[1], "% of space consumed"
            
            #waiting_func = raw_input("Press Enter to continue...")
            #print "resuming search..."            
            
            for i in range(fort_size):
                result_attempt[0][0][i].append("#")
            
            footer = ["#>"]
            for x in range(fort_size):
                footer.append("#")
            result_attempt[0][0].append(footer)
            
            save_item = raw_input("Keep this blueprint?(y/n/q)")
            
            if save_item == "y":
                multi_floor_selection.append(result_attempt[0][0])
            elif save_item == "q":
                clean_exit(multi_floor_selection)
            else:
                pass
             
    
    print "10,000 attempts completed."
    clean_exit(multi_floor_selection)

def fort_level_linker(multi_floor_selection):


    print len(multi_floor_selection), "total levels."
    for z in range(len(multi_floor_selection)):
        i_coord = []
        for x in range(len(multi_floor_selection[0])):
            for y in range(len(multi_floor_selection[0][0])):
                if multi_floor_selection[z][x][y] == "d":
                    try:
                        if multi_floor_selection[z+1][x][y] == "d":
                            i_coord.append([z,x,y])
                    except:
                        pass

        try:
            stairwell_coord = []
            stairwell_coord = i_coord[random.randint(0,len(i_coord)-1)]
        except:
            # This will actually fail to make a connection between these floors.
            pass 
        else:
            print "linking", z, "to", z+1, "... [", stairwell_coord[0], stairwell_coord[1], stairwell_coord[2], "]"
            multi_floor_selection[stairwell_coord[0]][stairwell_coord[1]][stairwell_coord[2]] = "i"
            multi_floor_selection[stairwell_coord[0]+1][stairwell_coord[1]][stairwell_coord[2]] = "i"

    return multi_floor_selection


def fort_writer(multi_floor_selection):
    """
    Add the correct quickfort buffers and write out the final fortress!
    """
    
    
    f = open("result_fort.csv", "wb")
    csv_w = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL)
    
    for each in multi_floor_selection:
        csv_w.writerows(each)

    f.close()
    print "A floor has been written."


def clean_exit(multi_floor_selection):
    
    print "Linking levels."
    multi_floor_selection = fort_level_linker(multi_floor_selection)
    print "Writing fort in QuickFort format."
    fort_writer(multi_floor_selection)
    print "exit(0)"
    sys.exit()



brute_force_selector(perc_dug_out, fort_depth, fort_size, node_depth)



