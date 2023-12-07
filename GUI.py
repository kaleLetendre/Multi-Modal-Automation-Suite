import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import shutil
import pyautogui

def upload_image():
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=(("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*")))
    if file_path:
        destination = os.path.join('images', os.path.basename(file_path))
        shutil.copy(file_path, destination)
        print(f"Image uploaded to {destination}.")


def upload_file():
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=(("Python files", "*.py"), ("All files", "*.*")))
    if file_path:
        destination = os.path.join('scripts', os.path.basename(file_path))
        shutil.copy(file_path, destination)
        print(f"File uploaded to {destination}.")

def start_script():
    global script_process
    script_process = subprocess.Popen(['python', 'auto_by_image.py'])
    print("Script started.")
    start_btn.config(state=tk.DISABLED)
    stop_btn.config(state=tk.NORMAL)

def stop_script():
    global script_process
    if script_process:
        script_process.terminate()
        print("Script stopped.")
        start_btn.config(state=tk.NORMAL)
        stop_btn.config(state=tk.DISABLED)

def collapse():
    # remove all the buttons
    image_btn.pack_forget()
    script_btn.pack_forget()
    start_btn.pack_forget()
    stop_btn.pack_forget()
    collapse_btn.pack_forget()
    # add the expand button
    expand_btn.pack(fill=tk.X)
    # set the alpha to 0.5
    root.attributes('-alpha', 0.5)


def expand():
    # remove the expand button
    expand_btn.pack_forget()
    # add all the buttons
    collapse_btn.pack(fill=tk.X)
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
image_btn = tk.Button(root, text="Upload Image", command=upload_image)
script_btn = tk.Button(root, text="Upload Script", command=upload_file)
start_btn = tk.Button(root, text="Play", command=start_script)
stop_btn = tk.Button(root, text="Pause", command=stop_script, state=tk.DISABLED)
collapse_btn = tk.Button(root, text="Hide", command=collapse)
expand_btn = tk.Button(root, text="+", command=expand)

# arrange the buttons in a grid
collapse_btn.pack(fill=tk.X)
image_btn.pack(fill=tk.X)
script_btn.pack(fill=tk.X)
start_btn.pack(fill=tk.X)
stop_btn.pack(fill=tk.X)




# Start the GUI event loop
root.mainloop()
