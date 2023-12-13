import os
import pyautogui
import cv2
import numpy as np
import time
import concurrent.futures
import multiprocessing
# Detect the number of CPU cores to set the optimal number of threads for concurrency
cpu_cores = multiprocessing.cpu_count()
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory).replace('\\', '/')
# settings.init()
master_values = settings.get_master_values()    


def process_image(image_name, sample_image):
    # read the image
    template_image = cv2.imread(f'{parent_directory}/images/{image_name}')
    # get the coordinates
    coordinates = locate_area(sample_image, template_image)
    # if coordinates are found
    if coordinates:
        # run the corresponding script with the top left coordinates and bottom right coordinates passed as 4 seperate command line arguments
        os.system(f'python -m package.scripts.{image_name.split(".")[0]} {coordinates[0][0]} {coordinates[0][1]} {coordinates[0][0] + coordinates[0][2]} {coordinates[0][1] + coordinates[0][3]}')
        return True
    return False

def screen_capture():
    # Take screenshot
    img = pyautogui.screenshot()
    # Convert to numpy array
    img = np.array(img)
    # Convert RGB to BGR
    img = img[:, :, ::-1].copy()
    return img
def locate_area(sample_image, template_image, threshold=0.5):
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
def click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()
def click_and_drag(x, y, x_prime, y_prime):
    pyautogui.moveTo(x, y)
    pyautogui.dragTo(x_prime, y_prime, duration=0.5)

# 2 folders, 1 containing the images to be found, the other containing python scripts with the same name
# when the image is found, the corresponding script is run with the top left coordinates and bottom right coordinates passed as arguments
def auto_by_image():
    # get screenshot
    sample_image = screen_capture()
    # loop through all the images in the folder
    with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_cores) as executor:
        for image_name in os.listdir(parent_directory + '/images'):
            future = executor.submit(process_image, image_name, sample_image)

while True:
    # try:
        auto_by_image()
        time.sleep(master_values['auto_by_image_delay'])
    # except Exception as e:
    #     time.sleep(0.1)
