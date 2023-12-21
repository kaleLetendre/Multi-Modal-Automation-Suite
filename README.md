# Multi-Modal Automation Suite

## Introduction

This Multi-Modal Automation Suite is a versatile and powerful tool designed for automated interactions with your computer, leveraging visual cues, state-based logic, and scheduled tasks. Ideal for a broad range of applications including automated testing, interactive monitoring, and gaming, this suite stands out with its ability to adapt to various triggers and scenarios.

## Core Components

* **Image-Based Automation (`auto_by_image.py`)** : Captures the screen in real-time and executes scripts when predefined images are detected. This component is crucial for tasks that require visual cue-based automation.
* **State-Driven Tasks (`auto_by_state.py`)** : Executes scripts based on the specific state conditions defined in `master_values.json`, allowing for complex, conditional automation workflows.
* **Scheduled Actions (`auto_by_schedule.py`)** : Manages and triggers tasks at pre-set times or intervals, adding a time-based dimension to the automation capabilities.

## Features

* **Versatile Task Handling** : Seamlessly handles a variety of tasks, from simple script execution upon image recognition to complex, conditional logic and time-based operations.
* **Asynchronous and Concurrent Processing** : Built with Python’s asyncio library, enhancing performance through efficient task management.
* **Dynamic Configuration** : Customizable through `master_values.json` for tailored operational control.
* **Planned GPU Acceleration** : Future updates aim to incorporate GPU acceleration, promising further improvements in processing efficiency, particularly in image recognition tasks.

## Setup and Usage

1. Fill the `images` folder with target images for monitoring.
2. Create corresponding Python scripts in the `scripts` folder; these will execute when matching images are detected.
3. Create state and schedule scripts in the `scripts` folder.
4. Configure operational parameters in `master_values.json` according to your needs.
5. Use the GUI to run the automation

## System Requirements

* A Python environment with necessary libraries such as pyautogui and opencv-python.
* (Optional) OpenCV with GPU support for future performance enhancements.

## Support the Creator

To support the development and enhancement of this project, consider visiting [Buy Me a Coffee](https://www.buymeacoffee.com/kaleletendre).

*Note: Please give credit and link back to this project if it is used elsewhere.*
