# PhotoCombiner
One of several little projects I did to practice some Python. Did it to prevent me from forgetting things after getting the Associated Python Programmer Certificate.
Used Python 3.11.4 and tkinter 8.6 


The program is used to combine photos of different sources (cameras) in one folder and name them in a way, that they sort in the correct chronological order.

![Alt Text](/docs/pics/screenshot.JPG?raw=true "screenshot")

### How it works

#### With Explorer or other tools:
- Create a work folder and in it a folder for each source (camera). Copy all pictures from each camera to the corresponding folder.
- Start PhotoCombiner

#### Button "...":
- Choose the working folder: \
![Alt Text](/docs/pics/folderstructure.JPG?raw=true "folderstructure")

#### Button "merge from sources":
Copies all pictures from all sources and renames them as follows: \
	IMG_[YEAR][MONTH][DAY]_[HOUR][MIN][SEC]__[ORIG.NAME]_[SOURCE]
	
- After the pictures have been merged, all pictures appear on the timeline, where they can be moved along the time axes.
- The pictures from each source appear with a different color
- The cursor shows the moving mode: "1" moving one pic at a time, "all" moving all pictures of one source together. Change mode with a right click in the timeline.
#### Button "rename moved pics"
After pictures have been moved along the time axis, they can be renamed according to where they have been moved.


### branches
main : the actual version \
picpreview: actual developing folder with picture preview according to timeline order\

