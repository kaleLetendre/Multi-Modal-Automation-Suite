# take top left and bottom right coordinates as command line arguments
import sys
import json
import package.auto_by.settings as settings

# read the top left and bottom right coordinates of the image ONLY HAVE THESE IF IT IS AN IMAGE AUTOMATION
try:
    top_left = (int(sys.argv[1]), int(sys.argv[2]))
    bottom_right = (int(sys.argv[3]), int(sys.argv[4]))
except:
    # print('no coordinates given defaulting to 0, 0')
    top_left = (0, 0)
    bottom_right = (0, 0)

# ______________________________CODE GOES HERE____________________________________
# use the coordinates and settings.master_values_main to do whatever you want
# be sure to update settings.master_values_main if you want to dynamically change the state of the program
if settings.master_values_main['seconds'] == 60:
    settings.master_values_main['seconds'] = 0
    try:
        settings.master_values_main['minutes'] = int(settings.master_values_main['minutes']) + 1
    except:
        settings.master_values_main['minutes'] = 1
    if settings.master_values_main['minutes'] == 60:
        settings.master_values_main['minutes'] = 0
        try:
            settings.master_values_main['hours'] = int(settings.master_values_main['hours']) + 1
        except:
            settings.master_values_main['hours'] = 1
        if settings.master_values_main['hours'] == 24:
            settings.master_values_main['hours'] = 0
            try:
                settings.master_values_main['days'] = int(settings.master_values_main['days']) + 1
            except:
                settings.master_values_main['days'] = 1
            if settings.master_values_main['days'] == 30:
                settings.master_values_main['days'] = 0
                try:
                    settings.master_values_main['months'] = int(settings.master_values_main['months']) + 1
                except:
                    settings.master_values_main['months'] = 1
                if settings.master_values_main['months'] == 12:
                    settings.master_values_main['months'] = 0
                    try:
                        settings.master_values_main['years'] = int(settings.master_values_main['years']) + 1
                    except:
                        settings.master_values_main['years'] = 1


# ________________________________________________________________________________