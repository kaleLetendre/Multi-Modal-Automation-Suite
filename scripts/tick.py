# take top left and bottom right coordinates as command line arguments
import sys


top_left = (int(sys.argv[1]), int(sys.argv[2]))
bottom_right = (int(sys.argv[3]), int(sys.argv[4]))

# read the master_values.txt file
# values are stored in the following format:
# valuename:value
master_values = {}
with open('master_values.txt', 'r') as f:
    # get the values
    values = f.read().split()
    # loop through the values
    for value in values:
        # split the value
        value = value.split(':')
        # add the value to the dictionary
        master_values[value[0]] = value[1]

try:
    master_values['tick'] = str(int(master_values['tick']) + 1)
except:
    master_values['tick'] = '0'

# write to the master_values.txt file
with open('master_values.txt', 'w') as f:
    # loop through the dictionary
    for key, value in master_values.items():
        # write the key and value to the file
        f.write(f'{key}:{value}\n')