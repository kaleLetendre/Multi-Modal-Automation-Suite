# take top left and bottom right coordinates as command line arguments
import sys
import json
import auto_by_basic

# read the top left and bottom right coordinates of the image ONLY HAVE THESE IF IT IS AN IMAGE AUTOMATION
try:
    top_left = (int(sys.argv[1]), int(sys.argv[2]))
    bottom_right = (int(sys.argv[3]), int(sys.argv[4]))
except:
    # print('no coordinates given defaulting to 0, 0')
    top_left = (0, 0)
    bottom_right = (0, 0)

master_values = auto_by_basic.get_master_values()


# ______________________________CODE GOES HERE____________________________________
# use the coordinates and master_values to do whatever you want
# be sure to update master_values if you want to dynamically change the state of the program
master_values['seconds'] = 0

# ________________________________________________________________________________


auto_by_basic.write_master_values(master_values)