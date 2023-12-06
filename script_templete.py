# take top left and bottom right coordinates as command line arguments
import sys

# read the top left and bottom right coordinates of the image
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

# ______________________________CODE GOES HERE____________________________________
# use the coordinates and master_values to do whatever you want
# be sure to update master_values if you want to dynamically change the state of the program


# ________________________________________________________________________________


# write to the master_values.txt file
with open('master_values.txt', 'w') as f:
    # loop through the dictionary
    for key, value in master_values.items():
        # write the key and value to the file
        f.write(f'{key}:{value}\n')