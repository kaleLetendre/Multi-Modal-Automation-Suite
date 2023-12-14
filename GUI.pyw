import asyncio
import json
import threading
import time
import tkinter as tk
from tkinter import scrolledtext
import auto_by
class AutomationGUI:
    def __init__(self, master):
        self.master = master
        master.title("Automation System")
        master.configure(bg='white')

        # Initialize flags for running states
        self.image_automation_running = False
        self.state_automation_running = False
        self.schedule_automation_running = False

        # Create auto_by instances
        self.auto_image = auto_by.auto_by_image()
        self.auto_state = auto_by.auto_by_state()
        self.auto_schedule = auto_by.auto_by_schedule()

        # Grid layout configuration
        master.grid_columnconfigure(3, weight=1)
        master.grid_rowconfigure(2, weight=1)

        # Styling Configuration
        start_button_style = {'bg': '#4cf554', 'fg': 'black', 'font': ('Helvetica', 10, 'bold'), 'padx': 10, 'pady': 5}
        stop_button_style = {'bg': '#f54c4c', 'fg': 'white', 'font': ('Helvetica', 10, 'bold'), 'padx': 10, 'pady': 5}
        config_editor_style = {'bg': '#a3a3a3', 'fg': 'black', 'font': ('Helvetica', 10, 'bold'), 'padx': 10, 'pady': 5}

        # Button Creation and Placement
        self.start_img_btn = self.create_button("Start Image Automation", self.start_image_automation, 1, 0, start_button_style)
        self.stop_img_btn = self.create_button("Stop Image Automation", self.stop_image_automation, 1, 0, stop_button_style, True)
        self.start_state_btn = self.create_button("Start State Automation", self.start_state_automation, 1, 1, start_button_style)
        self.stop_state_btn = self.create_button("Stop State Automation", self.stop_state_automation, 1, 1, stop_button_style, True)
        self.start_schedule_btn = self.create_button("Start Schedule Automation", self.start_schedule_automation, 1, 2, start_button_style)
        self.stop_schedule_btn = self.create_button("Stop Schedule Automation", self.stop_schedule_automation, 1, 2, stop_button_style, True)

        # Configuration Editor
        auto_by_thread = threading.Thread(target=self.run_auto_bys)
        auto_by_thread.start()

    def create_button(self, text, command, row, column, style, hide=False, name=""):
        button = tk.Button(self.master, text=text, command=command, **style)
        button.grid(row=row, column=column, sticky="ew", padx=5, pady=5)
        if hide:
            button.grid_remove()
        button.name = name
        return button
    
    def load_config(self):
        # Load configuration data into the editor
        while True:
            try:
                self.config_editor.delete('1.0', tk.END)
                with open('master_values.json', 'r') as file:
                    self.config_editor.insert(tk.INSERT, file.read())
            except FileNotFoundError:
                pass
            time.sleep(1)
    
    def drag_window(self, event):
        # Move the window
        x = self.master.winfo_pointerx() - self.master._offsetx
        y = self.master.winfo_pointery() - self.master._offsety
        self.master.geometry('+{x}+{y}'.format(x=x, y=y))
    
    def click_window(self, event):
        # Get the window offset
        self.master._offsetx = event.x
        self.master._offsety = event.y

    def release_window(self, event):
        # Clear the window offset
        self.master._offsetx = None
        self.master._offsety = None
    
    def iconify(self, event):
        # Minimize the window
        self.master.iconify()

    def start_image_automation(self):
        # Start image-based automation logic
        self.image_automation_running = True
        # make the stop button visible
        self.start_img_btn.grid_remove()
        self.stop_img_btn.grid()

    def stop_image_automation(self):
        # Stop image-based automation logic
        self.image_automation_running = False
        # make the start button visible
        self.stop_img_btn.grid_remove()
        self.start_img_btn.grid()
    
    def start_state_automation(self):
        # Start state-based automation logic
        self.state_automation_running = True
        self.start_state_btn.grid_remove()
        self.stop_state_btn.grid()
    
    def stop_state_automation(self):
        # Stop state-based automation logic
        self.state_automation_running = False
        self.stop_state_btn.grid_remove()
        self.start_state_btn.grid()
    
    def start_schedule_automation(self):
        # Start schedule-based automation logic
        
        self.schedule_automation_running = True
        self.start_schedule_btn.grid_remove()
        self.stop_schedule_btn.grid()

    
    def stop_schedule_automation(self):
        # Stop schedule-based automation logic
        
        self.schedule_automation_running = False
        self.stop_schedule_btn.grid_remove()
        self.start_schedule_btn.grid()

    def load_master_values(self):
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

    def run_auto_bys(self):
        # Run all auto_by scripts
        start_time = time.time()
        runs = 1
        # get the values from the master_values.json file
        # set the variable in auto_by to the value
        
        while True:
            master_values = self.load_master_values()
            self.auto_image.master_values = master_values
            self.auto_state.master_values = master_values
            self.auto_schedule.master_values = master_values
            runs += 1
            if self.state_automation_running:
                asyncio.run(self.auto_state.run())
            if self.image_automation_running:
                asyncio.run(self.auto_image.run())
            if self.schedule_automation_running:
                asyncio.run(self.auto_schedule.run((time.time() - start_time)/runs))
            latency = (time.time() - start_time)/runs
            if latency < 0.1:
                time.sleep(0.1 - latency)

    def on_closing(self):
        self.master.destroy()
        exit()

root = tk.Tk()
gui = AutomationGUI(root)
root.protocol("WM_DELETE_WINDOW", gui.on_closing)
root.mainloop()

