# take top left and bottom right coordinates as command line arguments
import sys
import json
import pyautogui

# use this to use basic auto_by functions
# this can be later used to create a VPL
# this can be used to define basic auto_by functions such as:

# - auto_by_basic.get_master_values()
# - auto_by_basic.write_master_values()

# - auto_by_basic.mouse_click()
# - auto_by_basic.mouse_release()
# - auto_by_basic.mouse_move()

# - auto_by_basic.key_press()
# - auto_by_basic.key_presses()

# - auto_by_basic.wait()
# - auto_by_basic.wait_until()

# - auto_by_basic.set_master_value(key, value)
# - auto_by_basic.get_master_value(key)



def get_master_values():
    # read the master_values.json file
    filename = 'master_values.json'
    master_values = {}
    with open(filename, 'r') as f:
        # get the values
        master_values = json.load(f)
    return master_values

def write_master_values(master_values):
    with open('master_values.json', 'w') as f:
        json.dump(master_values, f)

def mouse_click(x, y):
    pyautogui.mouseDown(x, y)

def mouse_release(x, y):
    pyautogui.mouseUp(x, y)

def mouse_move(x, y):
    pyautogui.moveTo(x, y)

def key_press(key):
    pyautogui.press(key)

def key_presses(keys):
    pyautogui.press(keys)

def wait(seconds):
    pyautogui.sleep(seconds)

def wait_until(condition):
    pyautogui.waitUntil(condition)

def set_master_value(key, value):
    master_values = get_master_values()
    master_values[key] = value
    write_master_values(master_values)

def get_master_value(key):
    master_values = get_master_values()
    return master_values[key]
