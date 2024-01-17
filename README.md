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

### Button "help"
shows this text

### zooming IN/OUT timeline
- place the cursor on the timeline where you want to zoom in or out and use the mouswheel
- alternatively use the long gray buttons in on top or bottom of the timeline. The horizontal position where you click the button determines the center of the zoom.

### pic/video preview
the preview always shows the picture or video correponding to the one the mouse last moved over in the timeline as well as 3 pictures before and after in the timeline.

### changing still preview picture of video
videos in the preview can be played forward and backward by holding the left or right mouse button down on them.


### branches
main : the actual version \
releaseWindows: version to create windows exe

