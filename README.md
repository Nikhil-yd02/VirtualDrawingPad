# VirtualDrawingPad

VDP (using OpenCV in python) is an application of image processing whereby an stylus(marker) is threshold from the background, its
centroid is calculated which works as a pen used to draw paintings on the screen which can also be erased.

## **Video link** : https://drive.google.com/drive/folders/1lrdtyMnID91wBrTwPnALep4KvEukZsun?usp=sharing


## Work flow:

#### STEP 1: Find the HSV range of the target stylus(Marker/pen).
#### STEP 2: Use the above values to start drawing in the main code.
#### STEP 3: We will use color masking to get a mask of our colored pen/marker using the above HSV range.
#### STEP 4: Using contour detection we detect and track the location of that pen,i.e get the x,y coordinates.
#### STEP 5: Draw a line by joining the x,y coordinates of pen’s previous location (location in the previous frame) with the new x,y points.
#### STEP 6: Add a feature to use the marker as an Eraser to erase unwanted lines.
#### STEP 7: Finally, add another feature to clear the entire Canvas/Screen.
