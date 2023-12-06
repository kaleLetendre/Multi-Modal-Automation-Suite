# take top left and bottom right coordinates as command line arguments
import sys


top_left = (int(sys.argv[1]), int(sys.argv[2]))
bottom_right = (int(sys.argv[3]), int(sys.argv[4]))

# write the cords to a file
with open('cords.txt', 'w') as f:
    f.write(f'{top_left[0]} {top_left[1]} {bottom_right[0]} {bottom_right[1]}')