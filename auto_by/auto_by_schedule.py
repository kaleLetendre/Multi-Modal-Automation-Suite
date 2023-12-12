# monitor the current time, down to the 1/10th of a second intervals
# if the current time is equal to the time in the schedule, run the script
# if the current time diff is greater than the rate, run the script
# there are 2 types of schedules, one that runs at a certain time, and one that runs at a certain rate

# all schedules have the prefix schedule_
# the schedule format is based on cron
# schedule_*;*;*;*;*;*;*.py is the format s, m, h, d, w, m, y
# for a schedule that runs every 5th of the month at 12:00:00, the schedule would be schedule_0;0;12;5;*;*;*.py
# for a schedule that runs every 5th and 20th of the month at 12:00:00, the schedule would be schedule_0;0;12;5,20;*;*;*.py

# all rates have the prefix rate_
# the rate format is based on value;unit;last_run
# value is an integer
# unit is ss, s, m, h, d, w, m, y for subseconds (1/10), seconds, minutes, hours, days, weeks, months, years
# last_run is the last time the script was run
# for example, rate_1;s;0.py would run the script every second
# for example, rate_1;m;0.py would run the script every minute
# the last_run value is the last time the script was run, in unix time this will look like rate_1;s;1609459200.py

import datetime
import concurrent.futures
import json
import multiprocessing
import os
import time
cpu_cores = multiprocessing.cpu_count()
filename = 'master_values.json'
master_values = {}
def process_schedule(script):
    name = script.split('schedule_')[1]
    name = name.split('.')[0]
    # get the current time and date in UTC 
    current_time = datetime.datetime.utcnow()
    current = [current_time.second, current_time.minute, current_time.hour, current_time.day, current_time.month, current_time.year]

    # get the schedule time and date
    schedule_time = name.split('_')[1]
    schedule = schedule_time.split(';')

    trigger = True
    # check if the current time matches the schedule time
    for i in range(0, 6):
        if schedule[i] != '*':
            if  "," in schedule[i]:
                # if any values match the current value, pass
                if int(current[i]) in [int(x) for x in schedule[i].split(',')]:
                    pass
                else:
                    trigger = False
                    break
            if int(schedule[i]) != current[i]:
                trigger = False
                break
    if trigger:
        # run the script
        os.system('python3 scripts/' + script)
    return
def process_rate(script):
    name = script.split('rate_')[1]
    if len(name.split('.')) > 2:
        # join 0 and 1
        name = name.split('.')[0] + '.' + name.split('.')[1]
    else:
        name = name.split('.')[0]
    # get the current unix time
    current_time = time.time()
    # get the rate value
    rate_value = name.split(';')[0]
    # get the rate unit
    rate_unit = name.split(';')[1]
    # get the last run time
    last_run = name.split(';')[2]
    # get the time diff
    time_diff = current_time - float(last_run)
    # get the time diff in seconds
    if rate_unit == 'ss':
        time_diff = time_diff * 10
    elif rate_unit == 's':
        time_diff = time_diff * 1
    elif rate_unit == 'm':
        time_diff = time_diff / 60
    elif rate_unit == 'h':
        time_diff = time_diff / 3600
    elif rate_unit == 'd':
        time_diff = time_diff / 86400
    elif rate_unit == 'w':
        time_diff = time_diff / 604800
    elif rate_unit == 'm':
        time_diff = time_diff / 2628000
    elif rate_unit == 'y':
        time_diff = time_diff / 31536000
        
    # check if the time diff is greater than the rate
    if time_diff >= int(rate_value):
        # rename the script with the current unix time
        os.rename(f'scripts/{script}', f'scripts/rate_{rate_value};{rate_unit};{current_time}.py')
        # run the script
        os.system('python scripts/rate_' + rate_value + ';' + rate_unit + ';' + str(current_time) + '.py')
    return
def auto_by_schedule():
    # get scripts
    scripts = os.listdir('scripts')
    # loop through all the images in the folder
    with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_cores) as executor:
        for script in scripts:
            name = script.split('.')[0]
            if "schedule_" in name:
                future = executor.submit(process_schedule, script)
                if future.result():
                    break
            elif "rate_" in name:
                future = executor.submit(process_rate, script)
                if future.result():
                    break
while True:
    try:
        try:
            with open(filename, 'r') as f:
                # get the values
                master_values = json.load(f)
        except:
            print('schedule master_values.json not found, creating it now')
            with open(filename, 'w') as f:
                master_values = {
                    'auto_by_schedule_delay': 0.1,
                    'auto_by_state_delay': 0.1,
                    'auto_by_image_delay': 0.1
                }
                json.dump(master_values, f)
        auto_by_schedule()
        time.sleep(master_values['auto_by_schedule_delay'])
    except Exception as e:
        print(e, 'sleeping for 0.1 seconds')
        time.sleep(0.1)
      


                