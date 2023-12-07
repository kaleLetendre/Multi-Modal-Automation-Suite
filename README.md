Automation System Overview
==========================

Introduction
------------

This automation system continuously monitors your computer screen for specific images and executes associated Python scripts when these images are detected. It's ideal for tasks like automated testing, monitoring, or gaming where specific visual cues trigger actions.

How it Works
------------

*   The main script, `auto_by_image.py`, runs in an infinite loop, capturing screenshots and analyzing them. These screenshots are temporarily stored in RAM for processing.
*   If a screenshot contains an area that matches at least 80% with any image in the `images` folder, the corresponding script in the `scripts` folder (with the same name as the image) is executed.
*   For example, if `tick.png` is detected on the screen, `tick.py` will be executed, and the script will receive the coordinates of where the image was found.

Features
--------

*   **Concurrent Processing**: Utilizes multi-threading to enhance performance, particularly in systems with multiple CPU cores.
*   **Dynamic Configuration**: Configurable settings are read from `master_values.json`. This includes the delay between screen captures and other potential settings.
*   **GPU Acceleration (Future Enhancement)**: Plans to incorporate GPU acceleration for systems with compatible hardware, to further improve image processing speeds.

Setup and Usage
---------------

1.  Place the images you want to monitor in the `images` folder.
2.  For each image, create a corresponding Python script in the `scripts` folder. This script will be executed when its associated image is detected.
3.  Adjust settings in `master_values.json` as needed.
4.  Run `auto_by_image.py` to start the automation or use the GUI to start it.

System Requirements
-------------------

*   Python environment with required libraries (`pyautogui`, `opencv-python`, etc.).
*   Optional: OpenCV with GPU support for future enhancements.

Contributing
------------

Contributions to enhance this project, such as adding GPU support or improving image processing algorithms, are welcome. Please follow standard GitHub pull request procedures.

Support the creator
------------
https://www.buymeacoffee.com/kaleletendw
