# Idea

* auto_by_image runs on a infinite loop taking screenshots of the screen and analyzing them (screenshots are only using inside ram)
* if an area of a screenshot is an 80% match of an image in the images folder, the script in the scripts folder with the same name as the image is ran as the result. For example if the image tick.png was located on the screen the script names tick.py would run and be passed the top left and bottom right coordinates of location the image was found at.
* images are analyzed on a multithreaded stream so filesize matters as well as order.
* race conditions and sequecing should be managed by master values
* scripts should store values in the master_values.txt file, this can be used to maintain overall state information (ex. only continue running a script if another script has activated a flag)

# Usage

simple examples are given im the images and scripts folder of the main branch.

for each image based action

* choose a name for the pair
* take a screenshot and put it in the images folder with the chosen name
* write a script that should be executed when that image is seen, and put it in the scripts folder

this allows flow between actions to be determined by state and not a predefined sequence
