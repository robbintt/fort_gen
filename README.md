fort_gen
========

An iterative fort generator for dwarf fortress.  Truly in alpha, fresh off the netbook.

why does this exist?  I believe it is more dwarfy to have less control over your dig designations.  Let the fort dig itself, guide it with yes/no decisions instead of inspiration!

The output of this is a multilevel QuickFort format .csv file suitable for auto-designating a dig.

I have some ideas for features, and please message me with ideas.

I wrote this in a caffeine binge and planned as I went. 
As such, functions are not yet as well defined as they should be in many cases.
Thanks for trying this out in alpha!

Please note: There are a few adjustable parameters in the top of fort_gen.py. Feel free to play with them.

Instructions:
0. put fort_gen.py and barefort.py in the same folder.

1. run fort_gen.py in linux.  Feel free to try it in windows as well, I haven't done so yet.

2. press yes for each floor you want to generate. If you don't want a floor, press 'n' or just hit enter.

3. after a few floors, or a lot of floors if you wish, press q to quit.

4. each floor will usually be linked by an up-down stairwell to the next and previous floors.

5. the fort will offload to a .csv file, which is in the quickfort format.

6. you may wish to manually edit the .csv file, but for the first try, I would just let it rip in QuickFort.
