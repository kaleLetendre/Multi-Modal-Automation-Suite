# monitor the current time, down to the 1/10th of a second intervals
# if the current time is equal to the time in the schedule, run the script
# if the current time diff is greater than the rate, run the script
# there are 2 types of schedules, one that runs at a certain time, and one that runs at a certain rate

# the schedule format is based on cron
# * * * * * * is the format for seconds, minutes, hours, days, months, years
# for example, 0 0 0 0 0 0 would run the script at midnight on the first day of the first month of the first year
# for example, 0 0 0 0 0 * would run the script at midnight on the first day of every month of every year
# for example, 0 0 0 0 * * would run the script at midnight on the first day of every month of every year

# the rate format is based on value;unit;last_run
# value is an integer
# unit is ss, s, m, h, d, w, m, y for subseconds (1/10), seconds, minutes, hours, days, weeks, months, years
# last_run is the last time the script was run
# for example, 1;s;0 would run the script every second
# for example, 1;m;0 would run the script every minute
# the last_run value is the last time the script was run, in unix time this will look like 1;s;1609459200.py