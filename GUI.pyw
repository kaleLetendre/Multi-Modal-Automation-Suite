import asyncio
import json
import threading
import time
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import auto_by
from tkinter import filedialog
import pyautogui
import os
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
        # label to notify the user that f7 starts all and f8 stops all
        
        # container to hold the status
        self.status_container = tk.Frame(self.master, bg='#b4b4b4')
        self.status_container.grid(row=0, column=0, sticky="nsew")
        
        # container to hold home
        self.container = tk.Frame(self.master, bg='white')
        self.container.grid(row=1, column=0, sticky="nsew")

        # container to hold the image upload
        self.image_container = tk.Frame(self.master, bg='white')
        self.image_container.grid(row=1, column=0, sticky="nsew")

        # container to hold the state upload
        self.state_container = tk.Frame(self.master, bg='white')
        self.state_container.grid(row=1, column=0, sticky="nsew")

        # container to hold the schedule upload
        self.schedule_container = tk.Frame(self.master, bg='white')
        self.schedule_container.grid(row=1, column=0, sticky="nsew")

        # make the non-home containers invisible
        self.state_container.grid_remove()
        self.schedule_container.grid_remove()
        self.image_container.grid_remove()
        
        # Grid layout configuration
        master.grid_columnconfigure(3, weight=1)
        master.grid_rowconfigure(2, weight=1)

        # Styling Configuration
        start_button_style = {'bg': '#9edba2', 'fg': 'black', 'font': ('Helvetica', 10, 'bold'), 'padx': 10, 'pady': 5}
        stop_button_style = {'bg': '#c48888', 'fg': 'black', 'font': ('Helvetica', 10, 'bold'), 'padx': 10, 'pady': 5}
        condition_button_style = {'bg': '#bebea6', 'fg': 'black', 'font': ('Helvetica', 10, 'bold'), 'padx': 10, 'pady': 5}
        upload_button_style = {'bg': '#b1c1c1', 'fg': 'black', 'font': ('Helvetica', 10, 'bold'), 'padx': 10, 'pady': 5}
        back_button_style = {'bg': '#bcbcbc', 'fg': 'black'}
        
        # ___STATUS CONTAINER___
        self.f_label = tk.Label(self.status_container, text="F7 starts all, F8 stops all", bg='#b4b4b4', fg='black', font=('Helvetica', 10, 'bold'))
        self.f_label.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.start_img_btn = self.create_button("Start Image Automation", self.start_image_automation, 1, 0, start_button_style, False, container=self.status_container)
        self.stop_img_btn = self.create_button("Stop Image Automation", self.stop_image_automation, 1, 0, stop_button_style, True, container=self.status_container)

        self.start_state_btn = self.create_button("Start State Automation", self.start_state_automation, 1, 1, start_button_style, False, container=self.status_container)
        self.stop_state_btn = self.create_button("Stop State Automation", self.stop_state_automation, 1, 1, stop_button_style, True, container=self.status_container)

        self.start_schedule_btn = self.create_button("Start Schedule Automation", self.start_schedule_automation, 1, 2, start_button_style, False, container=self.status_container)
        self.stop_schedule_btn = self.create_button("Stop Schedule Automation", self.stop_schedule_automation, 1, 2, stop_button_style, True, container=self.status_container)

        # ___HOME CONTAINER___
        self.upload_image_script_btn = self.create_button("Upload Image Script", self.upload_image_script, 2, 0, upload_button_style, False, container=self.container)

        self.upload_state_script_btn = self.create_button("Upload State Script", self.upload_state_script, 2, 1, upload_button_style, False, container=self.container)

        self.upload_schedule_script_btn = self.create_button("Upload Schedule Script", self.upload_schedule_script, 2, 2, upload_button_style, False, container=self.container)
        # make state and schedule buttons unclickable
        self.upload_state_script_btn.configure(state='disabled')
        self.upload_schedule_script_btn.configure(state='disabled')

        # ___IMAGE CONTAINER___
        self.image_back_btn = self.create_button("<", self.back_to_home, 0, 0, back_button_style, False, container=self.image_container)
        self.image_name_input_label = tk.Label(self.image_container, text="Name:", bg='white', fg='black', font=('Helvetica', 10, 'bold'))
        self.image_name_input = tk.Entry(self.image_container, bg='#b4b4b4', fg='black', font=('Helvetica', 10, 'bold'))
        # button to select script from filesystem
        self.image_script_label = tk.Label(self.image_container, text="No Script Selected", bg='white', fg='black', font=('Helvetica', 10, 'bold'))
        self.image_script_btn = self.create_button("Select Script", self.select_script, 1, 0, condition_button_style, False, "image_script_btn", container=self.image_container)
        # button to take screenshot
        self.screenshot_btn = self.create_button("Screen Shot", self.init_screenshot, 2, 0, condition_button_style, container=self.image_container)
        # image view
        self.image_view = tk.Label(self.image_container, bg='white', fg='black', font=('Helvetica', 10, 'bold'))
        # button to upload the pair
        self.image_script_upload_btn = self.create_button("Upload", self.upload_image_script_pair, 3, 0, condition_button_style, container=self.image_container)
        self.notification_label = tk.Label(self.image_container, text="", bg='white', fg='black', font=('Helvetica', 10, 'bold'))
        
        # ___STATE CONTAINER___

        
        # ___SCHEDULE CONTAINER___
  

        auto_by_thread = threading.Thread(target=self.run_auto_bys)
        auto_by_thread.start()

    def create_button(self, text, command, row, column, style, hide=False, name="", container=None):
        button = tk.Button(container, text=text, command=command, **style)
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
        self.auto_image = auto_by.auto_by_image()
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
        self.auto_state = auto_by.auto_by_state()
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
        self.auto_schedule = auto_by.auto_by_schedule()
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
        except:
            self.load_master_values()
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

    def init_screenshot(self):
        # make the container invisible
        self.image_container.grid_remove()
        # make the window fullscreen
        self.master.attributes('-fullscreen', True)
        try:
            # add the canvas
            canvas = self.master.children['!canvas']
            canvas.grid()
            canvas.delete('rect')
        except:
            canvas = tk.Canvas(self.master, bg='white')
            canvas.grid(row=0, column=0, sticky="nsew")

        # make the canvas fullscreen
        
        # make the canvas expand to fill the window
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        # force the window to the top
        self.master.attributes('-topmost', True)
        # make the window transparent
        self.master.attributes('-alpha', 0.3)
        # remove the border
        self.master.overrideredirect(True)
        # attach a listener to the mouse
        self.master.bind('<Button-1>', self.start_selection)
        self.master.bind('<B1-Motion>', self.size_selection)
        self.master.bind('<ButtonRelease-1>', self.confirm_selection)
        print('click and drag to select the area to screenshot')
    
    def start_selection(self, event):
        # get the coordinates of the click
        self.start_x = event.x_root
        self.start_y = event.y_root
        # unbind the listener
        self.master.unbind('<Button-1>')   
    
    def size_selection(self, event):
        # draw a rectangle on the canvas
        canvas = self.master.children['!canvas']
        # set the size of the canvas to the size of the window
        canvas.config(width=self.master.winfo_width(), height=self.master.winfo_height())
        try:
            canvas.delete('rect')
        except:
            pass
        canvas.create_rectangle(self.start_x, self.start_y, event.x_root, event.y_root, outline='red', width=3, tag='rect')
    
    def confirm_selection(self, event):
        self.end_x = event.x_root
        self.end_y = event.y_root
        try:
            # set alpha to 0
            self.master.attributes('-alpha', 0)
            self.screen_shot((self.start_x, self.start_y), (self.end_x, self.end_y))
        except Exception as e:
            print(e)
        # remove the listener
        self.master.unbind('<ButtonRelease-1>')
        self.master.unbind('<B1-Motion>')
        # remove the canvas
        canvas = self.master.children['!canvas']
        canvas.grid_remove()
        # make the window not fullscreen
        self.master.attributes('-fullscreen', False)
        # add the border
        self.master.overrideredirect(False)
        # remove the force top
        self.master.attributes('-topmost', False)
        # make the window not transparent
        self.master.attributes('-alpha', 1)
        # make the container visible
        self.image_container.grid()
        
    def screen_shot(self, top_left, bottom_right):
        # take a screenshot of the screen and crop it to the coordinates, promt the user for a name and save it to the images folder
        # open a file dialog to get the name
        try:
            screen_shot = pyautogui.screenshot()
            # crop the image
            screen_shot = screen_shot.crop((top_left[0], top_left[1], bottom_right[0], bottom_right[1]))
            # rescale the image to half size
            screen_shot.save("temp.png")
            # use PIL to display the image in the window
            image = Image.open('temp.png')
            image = ImageTk.PhotoImage(image)
            # rescale the image to half size
            image = image._PhotoImage__photo.subsample(2)
            self.image_view.image = image
            self.image_view.configure(image=image)

        except Exception as e:
            print(e)
    
    def upload_script(self,label):
        # open a file dialog to get the name
        try:
            file_name = filedialog.askopenfilename(initialdir = "./scripts",title = "Select file",filetypes = (("py files","*.py"),("all files","*.*")))
            # take the screenshot using pyautogui
            with open(file_name, 'r') as f:
                # get the values
                script = f.read()
            self.script_editor.delete('1.0', tk.END)
            self.script_editor.insert(tk.INSERT, script)
        except Exception as e:
            print(e)
    
    def back_to_home(self):
        try:
            self.image_container.grid_remove()
        except:
            pass
        try:
            self.state_container.grid_remove()
        except:
            pass
        try:
            self.schedule_container.grid_remove()
        except:
            pass
        self.container.grid()
    
    def upload_image_script(self):
        self.container.grid_remove()

        self.image_container.grid()

        # place the back button in the top left without use of grid
        self.image_back_btn.place(x=0, y=0, anchor='nw')
        # place a blank spacer in row 0 column 1
        self.spacer = tk.Label(self.image_container, bg='white', fg='black', font=('Helvetica', 10, 'bold'))
        self.spacer.grid(row=0, column=1, sticky="ew", padx=5, pady=5)


        self.image_name_input_label.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.image_name_input.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.image_script_btn.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.image_script_label.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        # set the label input in select_script to the label
        self.image_script_btn.configure(command=lambda: self.select_script(self.image_script_label))

        self.screenshot_btn.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.image_view.grid(row=3, column=1, sticky="ew", padx=5, pady=5, rowspan=4, columnspan=4)

        self.image_script_upload_btn.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        self.notification_label.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
    
    def upload_state_script(self):
        self.container.grid_remove()
        self.state_container.grid()
    
    def upload_schedule_script(self):
        self.container.grid_remove()
        self.schedule_container.grid()
    
    def select_script(self, label):
        # open a file dialog to get the name
        try:
            file_name = filedialog.askopenfilename(title = "Select script",filetypes = (("py files","*.py"),("all files","*.*")))
            with open(file_name, 'r') as f:
                # get the values
                script = f.read()
            # save as temp.py
            with open('temp.py', 'w') as f:
                f.write(script)
            label.configure(text=file_name)
        except Exception as e:
            print(e)

    def upload_image_script_pair(self):
        try:
            if self.image_name_input.get() == "":
                self.notification_label.configure(text="No Name Given", fg='red')

                return
            if not os.path.isfile('temp.py'):
                # set text to red
                self.notification_label.configure(text="No Script Selected", fg='red')
                return
            if not os.path.isfile('temp.png'):
                self.notification_label.configure(text="No Screenshot Taken", fg='red')
                return
            
            # take the name from the name input
            name = self.image_name_input.get()
            # get the temp.py file
            with open('temp.py', 'r') as f:
                # get the values
                script = f.read()
            # write the script to the scripts folder
            with open(f'scripts/{name}.py', 'w') as f:
                f.write(script)
            # get the temp.png file
            with open('temp.png', 'rb') as f:
                # get the values
                image = f.read()
            # write the image to the images folder
            with open(f'images/{name}.png', 'wb') as f:
                f.write(image)
            # remove the temp files

            os.remove('temp.py')
            os.remove('temp.png')

            self.notification_label.configure(text="Upload Successful", fg='green')
        except Exception as e:
            self.notification_label.configure(text="Upload Failed", fg='red')
            print(e)

    def stop_all(self, event):
        self.stop_image_automation()
        self.stop_state_automation()
        self.stop_schedule_automation()
    def start_all(self, event):
        self.start_image_automation()
        self.start_state_automation()
        self.start_schedule_automation()
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit? like really? like actually?"):
        root.destroy()
        exit()
# make f8 close the program
def close(event):
    on_closing()
# bind f8 to the close function
root = tk.Tk()
gui = AutomationGUI(root)
root.bind('<F8>', gui.stop_all)
root.bind('<F7>', gui.start_all)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

