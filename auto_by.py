import datetime
import os
import pyautogui
import cv2
import numpy as np
import time
import concurrent.futures
import json
import multiprocessing
cpu_cores = multiprocessing.cpu_count()
global master_values
filename = 'master_values.json'
def load_master_values():
    with open(filename, 'r') as f:
        # get the values
        master_values = json.load(f)
    return master_values
class auto_by_image:
    def __init__(self):
        self.filename = 'master_values.json'
    def process_image(self,image_name, sample_image):
        # read the image
        template_image = cv2.imread(f'images/{image_name}')
        # get the coordinates
        coordinates = self.locate_area(sample_image, template_image)
        # if coordinates are found
        if coordinates:
            # run the corresponding script with the top left coordinates and bottom right coordinates passed as 4 seperate command line arguments
            os.system(f'python scripts/{image_name[:-4]}.py {coordinates[0][0]} {coordinates[0][1]} {coordinates[0][0] + coordinates[0][2]} {coordinates[0][1] + coordinates[0][3]}')
            return True
        return False
    def screen_capture(self):
        # Take screenshot
        img = pyautogui.screenshot()
        # Convert to numpy array
        img = np.array(img)
        # Convert RGB to BGR
        img = img[:, :, ::-1].copy()
        return img
    def locate_area(self,sample_image, template_image, threshold=0.8):
        # find template in sample image
        result = cv2.matchTemplate(sample_image, template_image, cv2.TM_CCOEFF_NORMED)
        # get the coordinates of the template
        location = np.where(result >= threshold)
        # get the height and width of the template
        height, width = template_image.shape[:2]
        # create list of coordinates
        coordinates = []
        # loop through all the coordinates
        for x, y in zip(*location[::-1]):
            # add coordinates to list
            coordinates.append([x, y, width, height])
        # return coordinates
        return coordinates
    def run_auto_by_image(self):
        # get screenshot
        sample_image = self.screen_capture()
        with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_cores) as executor:
            for image_name in os.listdir('images'):
                future = executor.submit(self.process_image, image_name, sample_image)
                if future.result():
                    break
        return True

class auto_by_state:
    def __init__(self):
        self.filename = 'master_values.json'
        self.master_values = load_master_values()
    def process_state(self,script):
        name = script.split('state_')[1]
        name = name.split('.')[0]
        if "^" in name:
            # this is a script with multiple states
            states = name.split('^')
            for state in states:
                state_name = state.split(';')[0]
                desired_value = state.split(';')[1]
                try:
                    if str(master_values[state_name]) == desired_value:
                        # run the script
                        os.system('python scripts/' + script)
                except:
                    print('state not found')
        else:
            # this is a script with one state
            state_name = name.split(';')[0]
            desired_value = name.split(';')[1]
            if str(self.master_values[state_name]) == desired_value:
                # run the script
                os.system('python scripts/' + script)
        return
    def auto_by_state(self):
        self.master_values = load_master_values()
        scripts = os.listdir('scripts')
        # loop through all the images in the folder
        with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_cores) as executor:
            for script in scripts:
                name = script.split('.')[0]
                if "state_" in name:
                    future = executor.submit(self.process_state, script)
                    if future.result():
                        break
        return True

class auto_by_schedule:
    def __init__(self):
        pass
    def process_schedule(self,script):
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
    def process_rate(self,script, average_latency = 0):
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
        if time_diff + average_latency >= int(rate_value):
            # rename the script with the current unix time
            os.rename(f'scripts/{script}', f'scripts/rate_{rate_value};{rate_unit};{current_time}.py')
            # run the script
            os.system('python scripts/rate_' + rate_value + ';' + rate_unit + ';' + str(current_time) + '.py')
        return
    def run_auto_by_schedule(self, average_latency):
        # get scripts
        scripts = os.listdir('scripts')
        # loop through all the images in the folder
        with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_cores) as executor:
            for script in scripts:
                name = script.split('.')[0]
                if "schedule_" in name:
                    future = executor.submit(self.process_schedule, script)
                    if future.result():
                        break
                elif "rate_" in name:
                    future = executor.submit(self.process_rate, script, average_latency)
                    if future.result():
                        break
        return True
runs = 0
total_latency = 0
while True:
    runs += 1
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_cores) as executor:
            start_time = time.time()
            future1 = executor.submit(auto_by_image().run_auto_by_image)
            future2 = executor.submit(auto_by_state().auto_by_state)
            future3 = executor.submit(auto_by_schedule().run_auto_by_schedule, total_latency/runs)
            if future1.result():
                print(str(time.time() - start_time), end=' | ')
            if future2.result():
                print(str(time.time() - start_time), end=' | ')
            if future3.result():
                print(str(time.time() - start_time), end=' | ')
        print(str(time.time() - start_time), end='\r')
        total_latency += time.time() - start_time
    except Exception as e:
        print(e)