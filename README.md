auto_by_image runs on a infinite loop taking screenshots of the screen and analyzing them

if an area of a screenshot is an 80% match of an image in the images folder, the script in the scripts folder with the same name as the image is ran as the result

images are analyzed on a multithreaded stream so filesize matters more than order, race conditions and sequecing should be managed by master values

scripts should store values in the master_values.txt file, this can be used to maintain overall state information (ex. only continue running a script if another script has activated a flag)
