import asyncio
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
        config_editor_style = {'bg': '#f0f0f0', 'fg': '#333', 'insertbackground': 'black'}

        # Button Creation and Placement
        self.start_img_btn = self.create_button("Start Image Automation", self.start_image_automation, 0, 0, start_button_style)
        self.stop_img_btn = self.create_button("Stop Image Automation", self.stop_image_automation, 0, 0, stop_button_style, True)
        self.start_state_btn = self.create_button("Start State Automation", self.start_state_automation, 0, 1, start_button_style)
        self.stop_state_btn = self.create_button("Stop State Automation", self.stop_state_automation, 0, 1, stop_button_style, True)
        self.start_schedule_btn = self.create_button("Start Schedule Automation", self.start_schedule_automation, 0, 2, start_button_style)
        self.stop_schedule_btn = self.create_button("Stop Schedule Automation", self.stop_schedule_automation, 0, 2, stop_button_style, True)

        # Configuration Editor
        self.config_editor = scrolledtext.ScrolledText(master, height=10, **config_editor_style)
        self.config_editor.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.config_editor.tag_configure("json", foreground="blue")
        self.config_editor.tag_configure("string", foreground="green")
        self.config_editor.tag_configure("number", foreground="red")
        self.config_editor.tag_configure("boolean", foreground="orange")

        # Config live-update thread
        config_thread = threading.Thread(target=self.load_config)
        config_thread.start()

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
    
    def start_image_automation(self):
        # Start image-based automation logic
        self.image_automation_running = True
        # make the stop button visible
        self.start_img_btn.grid_remove()
        self.stop_img_btn.grid()
        run_auto_by_image_thread = threading.Thread(target=self.run_auto_by_image_thread)
        run_auto_by_image_thread.start()

    def stop_image_automation(self):
        # Stop image-based automation logic
        self.image_automation_running = False
        # make the start button visible
        self.stop_img_btn.grid_remove()
        self.start_img_btn.grid()
    
    def run_auto_by_image_thread(self):
        while self.image_automation_running:
            asyncio.run(self.auto_image.run())
        
    def start_state_automation(self):
        # Start state-based automation logic
        self.state_automation_running = True
        self.start_state_btn.grid_remove()
        self.stop_state_btn.grid()
        run_auto_by_state_thread = threading.Thread(target=self.run_auto_by_state_thread)
        run_auto_by_state_thread.start()
    
    def stop_state_automation(self):
        # Stop state-based automation logic
        self.state_automation_running = False
        self.stop_state_btn.grid_remove()
        self.start_state_btn.grid()
    
    def run_auto_by_state_thread(self):
        while self.state_automation_running:
            asyncio.run(self.auto_state.run())
        
    def start_schedule_automation(self):
        # Start schedule-based automation logic
        
        self.schedule_automation_running = True
        self.start_schedule_btn.grid_remove()
        self.stop_schedule_btn.grid()
        run_auto_by_schedule_thread = threading.Thread(target=self.run_auto_by_schedule_thread)
        run_auto_by_schedule_thread.start()
    
    def stop_schedule_automation(self):
        # Stop schedule-based automation logic
        
        self.schedule_automation_running = False
        self.stop_schedule_btn.grid_remove()
        self.start_schedule_btn.grid()
    
    def run_auto_by_schedule_thread(self):
        start_time = time.time()
        runs = 1
        while self.schedule_automation_running:
            asyncio.run(self.auto_schedule.run((time.time() - start_time)/runs))
            runs += 1

    def on_closing(self):
        self.master.destroy()
        exit()

root = tk.Tk()
gui = AutomationGUI(root)
root.protocol("WM_DELETE_WINDOW", gui.on_closing)

root.mainloop()

