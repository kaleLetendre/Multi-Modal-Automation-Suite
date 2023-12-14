# take top left and bottom right coordinates as command line arguments
import sys
import json

# read the top left and bottom right coordinates of the image
top_left = (int(sys.argv[1]), int(sys.argv[2]))
bottom_right = (int(sys.argv[3]), int(sys.argv[4]))

# read the master_values.json file
filename = 'master_values.json'
master_values = {}
with open(filename, 'r') as f:
    # get the values
    master_values = json.load(f)

try:
    master_values['tick'] = int(master_values['tick']) + 1
except:
    master_values['tick'] = 0

# write to the master_values.txt file
with open('master_values.json', 'w') as f:
    json.dump(master_values, f)