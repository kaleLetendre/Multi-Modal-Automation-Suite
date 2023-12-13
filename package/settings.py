import json
import threading
import time
import os
import sys

# create a python class to store the values
class settings:
    def __init__(self, filename='master_values.json'):
        self.filename = filename
        self.master_values_main = None
    def init(self):
        self.master_values_main = {}
        try:
            if self.master_values_main['init_has_run']:
                print('init has already run')
                return self.master_values_main
        except:
            print('init')
            # read the json file
            self.read_json()
        
    def read_json(self):
        try:
            with open(self.filename, 'r') as f:
                # get the values
                self.master_values_main = json.load(f)
        except Exception as e:
            print(e)
            print('master_values.json not found, creating it now')
            with open(self.filename, 'w') as f:
                self.master_values_main = {
                    'auto_by_schedule_delay': 0.1,
                    'auto_by_state_delay': 0.1,
                    'auto_by_image_delay': 0.1,
                    'init_has_run': True
                }
                json.dump(self.master_values_main, f)
    
    def upload_loop(self):
        print('upload loop started')
        while True:
            print('self.master_values_main', self.master_values_main)
            with open(self.filename, 'w') as f:
                json.dump(self.master_values_main, f)
            time.sleep(1)

    def get_master_values(self):
        print('get master values', self.master_values_main)
        return self.master_values_main

    def set_master_values(self, master_values):
        self.master_values_main = master_values
        print('set master values', self.master_values_main)
        return self.master_values_main
