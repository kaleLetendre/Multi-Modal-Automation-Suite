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
import json
import os
import time

# read the master_values.json file
master_values = {}
filename = 'master_values.json'
while True:
    try:
        with open(filename, 'r') as f:
            # get the values
            master_values = json.load(f)
    except:
        print('master_values.json not found, creating it now')
        with open(filename, 'w') as f:
            master_values = {
                'auto_by_schedule_delay': 0.1,
                'auto_by_state_delay': 0.1,
                'auto_by_image_delay': 0.1
            }
            json.dump(master_values, f)


    # iterate through the scripts in the scripts folder
    scripts = os.listdir('scripts')

    for script in scripts:
        name = script.split('.')[0]
        if "schedule_" in name:
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
        elif "rate_" in name:
            # get the current unix time
            current_time = time.time()
            name = name.split('_')[1]
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
                time_diff = time_diff
            elif rate_unit == 's':
                time_diff = time_diff / 10
            elif rate_unit == 'm':
                time_diff = time_diff / 600
            elif rate_unit == 'h':
                time_diff = time_diff / 36000
            elif rate_unit == 'd':
                time_diff = time_diff / 864000
            elif rate_unit == 'w':
                time_diff = time_diff / 6048000
            elif rate_unit == 'm':
                time_diff = time_diff / 25920000
            elif rate_unit == 'y':
                time_diff = time_diff / 311040000
            # check if the time diff is greater than the rate
            if time_diff >= int(rate_value):
                # rename the script with the current unix time
                os.rename(f'scripts/{script}', f'scripts/rate_{rate_value};{rate_unit};{current_time}.py')
                # run the script
                os.system('python3 scripts/rate_' + rate_value + ';' + rate_unit + ';' + str(current_time) + '.py')
    try:
        time.sleep(master_values['auto_by_schedule_delay'])
    except:
        print('auto_by_schedule_delay not found in master_values.json, adding it now using default value of 0.1')
        master_values['auto_by_schedule_delay'] = 0.1
        with open('master_values.json', 'w') as f:
            json.dump(master_values, f)
      


                