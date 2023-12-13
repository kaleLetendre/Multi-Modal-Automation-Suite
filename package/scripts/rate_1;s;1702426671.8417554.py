# take top left and bottom right coordinates as command line arguments
import sys
import package.auto_by.settings as settings
settings.init()
# read the top left and bottom right coordinates of the image ONLY HAVE THESE IF IT IS AN IMAGE AUTOMATION
try:
    top_left = (int(sys.argv[1]), int(sys.argv[2]))
    bottom_right = (int(sys.argv[3]), int(sys.argv[4]))
except:
    # print('no coordinates given defaulting to 0, 0')
    top_left = (0, 0)
    bottom_right = (0, 0)

# ______________________________CODE GOES HERE____________________________________
# use the coordinates and master_values to do whatever you want
# be sure to update master_values if you want to dynamically change the state of the program
try:
    settings.master_values_main['seconds'] = int(settings.master_values_main['seconds']) + 1
except:
    settings.master_values_main['seconds'] = 1

# ________________________________________________________________________________
