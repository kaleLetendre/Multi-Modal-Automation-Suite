
# if a certain state is found, run the corresponding script
# I need a way to correlate the state with the script
# all state scripts are prefixed with state_
# script name will be state_state_name;desired_value^second_state_name;desired_value.py
# format is, for each state value pair, state_name;desired_value, if there are multiple state value pairs, they are seperated by a ^, and the file extension is .py

import concurrent.futures
import multiprocessing
import os
import time
import settings
cpu_cores = multiprocessing.cpu_count()
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory).replace('/', '/')

def process_state(script):
    name = script.split('state_')[1]
    name = name.split('.')[0]
    if "^" in name:
        # this is a script with multiple states
        states = name.split('^')
        for state in states:
            state_name = state.split(';')[0]
            desired_value = state.split(';')[1]
            try:
                if str(settings.master_values_main[state_name]) == desired_value:
                    # run the script
                    os.system('python -m package.scripts.' + script.split('.')[0])
            except:
                print('state not found')
    else:
        # this is a script with one state
        state_name = name.split(';')[0]
        desired_value = name.split(';')[1]
        if str(settings.master_values_main[state_name]) == desired_value:
            # run the script
            os.system('python -m package.scripts.' + script.split('.')[0])
    return
def auto_by_state():
    scripts = os.listdir(parent_directory + '/scripts')
    # loop through all the images in the folder
    with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_cores) as executor:
        for script in scripts:
            name = script.split('.')[0]
            if "state_" in name:
                future = executor.submit(process_state, script)
                if future.result():
                    break
             
while True:
    try:
        # try:
        #     with open(filename, 'r') as f:
        #         # get the values
        #         master_values = json.load(f)
        # except Exception as e:
        #     print(e)
        #     print('state master_values.json not found, creating it now')
        #     with open(filename, 'w') as f:
        #         master_values = {
        #             'auto_by_schedule_delay': 0.1,
        #             'auto_by_state_delay': 0.1,
        #             'auto_by_image_delay': 0.1
        #         }
        #         json.dump(master_values, f)
        auto_by_state()
        time.sleep(settings.master_values_main['auto_by_state_delay'])
    except Exception as e:
        time.sleep(0.1)