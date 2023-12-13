# take top left and bottom right coordinates as command line arguments
import sys
import json
import package.auto_by.settings as settings

master_values = settings.get_master_values()
# read the top left and bottom right coordinates of the image
top_left = (int(sys.argv[1]), int(sys.argv[2]))
bottom_right = (int(sys.argv[3]), int(sys.argv[4]))



try:
    master_values['tick'] = int(master_values['tick']) + 1
except:
    master_values['tick'] = 0

settings.set_master_values(master_values)