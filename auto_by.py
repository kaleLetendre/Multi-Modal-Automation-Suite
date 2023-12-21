import datetime
import os
import pyautogui
import cv2
import numpy as np
import time
import json
import multiprocessing
import asyncio
import cProfile
import pstats

cpu_cores = multiprocessing.cpu_count()
global master_values
filename = 'master_values.json'
active = {"auto_by_image": False, "auto_by_state": False, "auto_by_schedule": False}
def load_master_values():
    try:
        with open('master_values.json', 'r') as f:
            # get the values
            master_values = json.load(f)
    except FileNotFoundError:
        # create the file
        with open('master_values.json', 'w') as f:
            # create the file
            master_values = {}
            json.dump(master_values, f)
    return master_values
class auto_by_image:
    def __init__(self):
        self.filename = 'master_values.json'
        self.template_images = self.load_template_images()
        self.master_values = load_master_values()

    def load_template_images(self):
        templates = {}
        for image_name in os.listdir('images'):
            template = cv2.imread(f'images/{image_name}')
            templates[image_name] = template
        return templates
    def reduce_resolution(self, image, scale_percent):
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return cv2.resize(resized, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_AREA)

    async def process_image(self, image_name, sample_image):
        template_image = self.template_images[image_name]
        template_image = self.reduce_resolution(template_image, 80)  # Example: reducing resolution by 50%
        sample_image = self.reduce_resolution(sample_image, 80)
        # get the coordinates
        coordinates = self.locate_area(sample_image, template_image)
        # if coordinates are found
        if coordinates:
            await asyncio.create_subprocess_shell(f'python scripts/{image_name[:-4]}.py {coordinates[0][0]} {coordinates[0][1]} {coordinates[0][0] + coordinates[0][2]} {coordinates[0][1] + coordinates[0][3]}')
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
    async def run(self):
        sample_image = self.screen_capture()
        tasks = [self.process_image(image_name, sample_image) for image_name in self.template_images]
        await asyncio.gather(*tasks)
        return True

class auto_by_state:
    def __init__(self):
        self.filename = 'master_values.json'
        self.master_values = load_master_values()
        self.temp = os.listdir('scripts')
        self.scripts = []
        for script in self.temp:
            # remove scripts that are not states
            if "state_" in script:
                self.scripts.append(script)
    async def process_state(self,script):
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
                        await asyncio.create_subprocess_shell(f'python scripts/{script}')
                except:
                    print('state not found')
        else:
            # this is a script with one state
            state_name = name.split(';')[0]
            desired_value = name.split(';')[1]
            if str(self.master_values[state_name]) == desired_value:
                # run the script
                await asyncio.create_subprocess_shell(f'python scripts/{script}')
                return
    async def run(self):
        for script in self.scripts:
            name = script.split('.')[0]
            if "state_" in name:
                await self.process_state(script)
        return True

class auto_by_schedule:
    def __init__(self):
        self.scripts = os.listdir('scripts')
        self.schedule_scripts = []
        self.rate_scripts = []
        self.master_values = load_master_values()
        for script in self.scripts:
            if "schedule_" in script:
                self.schedule_scripts.append(script)
            elif "rate_" in script:
                self.rate_scripts.append(script)
    async def process_schedule(self,script):
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
            await asyncio.create_subprocess_shell(f'python scripts/{script}')
        return
    async def process_rate(self,script, average_latency = 0):
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
            # change the name of the script in the list
            self.rate_scripts[self.rate_scripts.index(script)] = f'rate_{rate_value};{rate_unit};{current_time}.py'
            # run the script
            await asyncio.create_subprocess_shell(f'python scripts/rate_{rate_value};{rate_unit};{current_time}.py')
        return
    async def run(self, average_latency):
        # loop through all the images in the folder
        for script in self.schedule_scripts:
            name = script.split('.')[0]
            await self.process_schedule(script)
        for script in self.rate_scripts:
            name = script.split('.')[0]
            await self.process_rate(script, average_latency)
        return True
    
def main(image, state, schedule):
    auto_image = auto_by_image()
    auto_state = auto_by_state()
    auto_schedule = auto_by_schedule()  # Assuming you have this class
    runs = 0
    total_latency = 0
    runs += 1
    start_time = time.time()

    # execute the tasks concurrently
    tasks = []
    if image:
        tasks.append(auto_image.run())
    if state:
        tasks.append(auto_state.run())
    if schedule:
        tasks.append(auto_schedule.run(total_latency/runs))
    asyncio.gather(*tasks)
    latency = time.time() - start_time
    print(f"Average Latency: {total_latency/runs:.2f} seconds", end='\r')
    if latency < 0.1:
        asyncio.sleep(0.01 - latency)
        latency = 0.1
    total_latency += latency


