# monitor the master_values.json file
# if a certain state is found, run the corresponding script
# I need a way to correlate the state with the script
# all state scripts are prefixed with state_
# script name will be state_state_name;desired_value^second_state_name;desired_value.py
# format is, for each state value pair, state_name;desired_value, if there are multiple state value pairs, they are seperated by a ^, and the file extension is .py

import json
import os
import time

filename = 'master_values.json'
master_values = {}
while True:
    # read the master_values.json file
    try:
        try:
            with open(filename, 'r') as f:
                # get the values
                master_values = json.load(f)
        except:
            print('master_values.json not found, creating it now')
            with open(filename, 'w') as f:
                master_values = {
                    'auto_by_state_delay': 0.1
                }
                json.dump(master_values, f)
    except:
        print('auto_by_image_delay not found in master_values.json, adding it now using default value of 0.1')
        master_values['auto_by_state_delay'] = 0.1
        with open('master_values.json', 'w') as f:
            json.dump(master_values, f)

    # iterate through the scripts in the scripts folder
    scripts = os.listdir('scripts')

    for script in scripts:
        name = script.split('.')[0]
        if "state_" in name:
            if "^" in name:
                # this is a script with multiple states
                states = name.split('^')
                for state in states:
                    state_name = state.split(';')[0]
                    desired_value = state.split(';')[1]
                    try:
                        if master_values[state_name] == desired_value:
                            # run the script
                            os.system('python3 scripts/' + script)
                    except:
                        print('state not found')
            else:
                # this is a script with one state
                state_name = name.split(';')[0]
                desired_value = name.split(';')[1]
                try:
                    if master_values[state_name] == desired_value:
                        # run the script
                        os.system('python3 scripts/' + script)
                except:
                    print('state not found')
    time.sleep(master_values['auto_by_state_delay'])