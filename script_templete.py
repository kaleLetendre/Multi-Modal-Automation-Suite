# take top left and bottom right coordinates as command line arguments
import sys
import json

# read the top left and bottom right coordinates of the image
top_left = (int(sys.argv[1]), int(sys.argv[2]))
bottom_right = (int(sys.argv[3]), int(sys.argv[4]))

# read the master_values.json file
filename = 'master_values.json'
master_values = {}
try:
    with open(filename, 'r') as f:
        # get the values
        master_values = json.load(f)
except:
    print('master_values.json not found, creating it now')
    with open(filename, 'w') as f:
        master_values = {
            'auto_by_image_delay': 0.1
        }
        json.dump(master_values, f)

# ______________________________CODE GOES HERE____________________________________
# use the coordinates and master_values to do whatever you want
# be sure to update master_values if you want to dynamically change the state of the program


# ________________________________________________________________________________


# write to the master_values.txt file
with open('master_values.json', 'w') as f:
    json.dump(master_values, f)