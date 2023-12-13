import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import shutil
import pyautogui

def upload_image():
    # get the file (any file)
    filename = filedialog.askopenfilename(title="Select an Image", filetypes=(("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*")))
    # copy the file to the images folder and change the name to the name in the name_input
    shutil.copy(filename, f'images/{name_input.get()}.jpg')
    #print(f'Copied {filename} to images folder')


def upload_file():
    # get the script file
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("python files","*.py"),("all files","*.*")))
    # copy the file to the scripts folder and change the name to the name in the name_input
    shutil.copy(filename, f'scripts/{name_input.get()}.py')
    #print(f'Copied {filename} to scripts folder')
    

def start_script():
    global script_process
    script_process = subprocess.Popen(['python', 'auto_by.py'])
    #print("Script started.")
    start_btn.config(state=tk.DISABLED)
    stop_btn.config(state=tk.NORMAL)

def stop_script():
    global script_process
    if script_process:
        script_process.terminate()
        #print("Script stopped.")
        start_btn.config(state=tk.NORMAL)
        stop_btn.config(state=tk.DISABLED)

def collapse():
    # remove all the buttons
    image_btn.pack_forget()
    script_btn.pack_forget()
    start_btn.pack_forget()
    stop_btn.pack_forget()
    collapse_btn.pack_forget()
    name_input.pack_forget()
    # add the expand button
    expand_btn.pack(fill=tk.X)
    # set the alpha to 0.5
    root.attributes('-alpha', 0.5)


def expand():
    # remove the expand button
    expand_btn.pack_forget()
    # add all the buttons
    collapse_btn.pack(fill=tk.X)
    name_input.pack(fill=tk.X)
    image_btn.pack(fill=tk.X)
    script_btn.pack(fill=tk.X)
    start_btn.pack(fill=tk.X)
    stop_btn.pack(fill=tk.X)
    root.attributes('-alpha', 1)
    

# Set up the main window
root = tk.Tk()
# remove the title bar
root.overrideredirect(True)
# force the window to be on top
root.wm_attributes("-topmost", True)
# dont show the window in the taskbar
root.wm_attributes("-toolwindow", True)


# Add buttons and layout
# input for name to save the image and script with a default value of 'name'
name_input = tk.Entry(root)
name_input.insert(0, 'Name')
# center the text
name_input.config(justify=tk.CENTER)
image_btn = tk.Button(root, text="Upload Image", command=upload_image)
script_btn = tk.Button(root, text="Upload Script", command=upload_file)
start_btn = tk.Button(root, text="Play", command=start_script)
stop_btn = tk.Button(root, text="Pause", command=stop_script, state=tk.DISABLED)
collapse_btn = tk.Button(root, text="^", command=collapse)
expand_btn = tk.Button(root, text="+", command=expand)

# change the button colors
image_btn.config(bg='#393939')
script_btn.config(bg='#393939')
start_btn.config(bg='#393939')
stop_btn.config(bg='#393939')
collapse_btn.config(bg='#393939')
expand_btn.config(bg='#393939')
# change the button text colors
image_btn.config(fg='#d6d6d6')
script_btn.config(fg='#d6d6d6')
start_btn.config(fg='#d6d6d6')
stop_btn.config(fg='#d6d6d6')
collapse_btn.config(fg='#d6d6d6')
expand_btn.config(fg='#d6d6d6')


collapse_btn.pack(fill=tk.X)
name_input.pack(fill=tk.X)
image_btn.pack(fill=tk.X)
script_btn.pack(fill=tk.X)
start_btn.pack(fill=tk.X)
stop_btn.pack(fill=tk.X)




# Start the GUI event loop
root.mainloop()
