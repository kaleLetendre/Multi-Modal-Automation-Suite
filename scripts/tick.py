# take top left and bottom right coordinates as command line arguments
import sys
import json
import auto_by_basic

# read the top left and bottom right coordinates of the image
top_left = (int(sys.argv[1]), int(sys.argv[2]))
bottom_right = (int(sys.argv[3]), int(sys.argv[4]))

master_values = auto_by_basic.get_master_values()

try:
    master_values['tick'] = int(master_values['tick']) + 1
except:
    master_values['tick'] = 0

auto_by_basic.write_master_values(master_values)