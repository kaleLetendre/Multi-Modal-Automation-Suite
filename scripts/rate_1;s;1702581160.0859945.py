# take top left and bottom right coordinates as command line arguments
import sys
import json

# read the top left and bottom right coordinates of the image ONLY HAVE THESE IF IT IS AN IMAGE AUTOMATION
try:
    top_left = (int(sys.argv[1]), int(sys.argv[2]))
    bottom_right = (int(sys.argv[3]), int(sys.argv[4]))
except:
    # print('no coordinates given defaulting to 0, 0')
    top_left = (0, 0)
    bottom_right = (0, 0)
# read the master_values.json file
filename = 'master_values.json'
master_values = {}
with open(filename, 'r') as f:
    # get the values
    master_values = json.load(f)

# ______________________________CODE GOES HERE____________________________________
# use the coordinates and master_values to do whatever you want
# be sure to update master_values if you want to dynamically change the state of the program
try:
    master_values['seconds'] = int(master_values['seconds']) + 1
except:
    master_values['seconds'] = 1

# ________________________________________________________________________________


# write to the master_values.txt file
with open('master_values.json', 'w') as f:
    json.dump(master_values, f)