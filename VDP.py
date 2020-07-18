import numpy as np
import cv2 as cv


def nothing(x):
    pass


print('Enter e:switch between eraser and pen.')
print('Enter c:clear pad.')
print('Enter Esc To exit.')

cap = cv.VideoCapture(0)

# creating track bar to find threshold for mask:
cv.namedWindow('TrackBar', 0)
cv.resizeWindow('TrackBar', 256, 256)
cv.createTrackbar('L-H', 'TrackBar', 0, 255, nothing)
cv.createTrackbar('L-S', 'TrackBar', 0, 255, nothing)
cv.createTrackbar('L-V', 'TrackBar', 0, 255, nothing)
cv.createTrackbar('U-H', 'TrackBar', 0, 255, nothing)
cv.createTrackbar('U-S', 'TrackBar', 0, 255, nothing)
cv.createTrackbar('U-V', 'TrackBar', 0, 255, nothing)

# creating track bar for color and thickness of brush:
cv.namedWindow('COLOR TrackBar', 0)
cv.resizeWindow('COLOR TrackBar', 256, 256)
cv.createTrackbar('B', 'COLOR TrackBar', 0, 255, nothing)
cv.createTrackbar('G', 'COLOR TrackBar', 0, 255, nothing)
cv.createTrackbar('R', 'COLOR TrackBar', 0, 255, nothing)
cv.createTrackbar('THICKNESS', 'COLOR TrackBar', 1, 20, nothing)

# creating canvas/pad:
canvas = None

# used to toggle between pen and eraser:
val = 1

# Initial pos of pen:
x1, y1 = 0, 0

while True:
    _, frame = cap.read()
    frame = cv.flip(frame, 1)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    blur = cv.GaussianBlur(hsv, (5, 5), 100)

    # get current positions of Track-bar:
    lh = cv.getTrackbarPos('L-H', 'TrackBar')
    ls = cv.getTrackbarPos('L-S', 'TrackBar')
    lv = cv.getTrackbarPos('L-V', 'TrackBar')
    uh = cv.getTrackbarPos('U-H', 'TrackBar')
    us = cv.getTrackbarPos('U-S', 'TrackBar')
    uv = cv.getTrackbarPos('U-V', 'TrackBar')

    # get current positions of color Track-bar:
    b = cv.getTrackbarPos('B', 'COLOR TrackBar')
    g = cv.getTrackbarPos('G', 'COLOR TrackBar')
    r = cv.getTrackbarPos('R', 'COLOR TrackBar')
    t = cv.getTrackbarPos('THICKNESS', 'COLOR TrackBar')

    lower = np.array([lh, ls, lv])
    upper = np.array([uh, us, uv])
    mask = cv.inRange(blur, lower, upper)
    mask = cv.dilate(mask, (5, 5), iterations=1)

    cv.imshow('mask', mask)

    # Detecting contours of the mask:
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # creating the canvas for drawing if not already there:
    if canvas is None:
        canvas = np.zeros_like(frame)

    # if contour area is not None and is greater than 100 draw the line:
    if contours and cv.contourArea(max(contours, key=cv.contourArea)) > 100:
        c = max(contours, key=cv.contourArea)
        x2, y2, w, h = cv.boundingRect(c)

        # getting centroid of stylus/mask bounding rectangle:
        x2, y2 = x2+(w//2), y2+(h//2)

        # projecting dot as centroid on frame for reference to draw:
        cv.circle(frame, (x2, y2), 10, (255, 0, 255), -1)

        if x1 == 0 and y1 == 0:
            # if x1 and y1 are the only points or at initial time allot first point:
            x1, y1 = x2, y2
        else:
            # draw line on the canvas:
            canvas = cv.line(canvas, (x1, y1), (x2, y2), [b*val, g*val, r*val], t)
        # new point becomes previous point:
        x1, y1 = x2, y2
    else:
        # restart when a stylus is avaliable:
        x1, y1 = 0, 0

    # Displaying the result:
    cv.imshow('canvas', canvas)
    cv.imshow('frame', frame)

    k = cv.waitKey(1) & 0xFF
    if k == 27:
        # exit the program:
        break
    elif k == ord('c'):
        # clear the canvas:
        canvas = None
    elif k == ord('e'):
        # Switch between eraser and pen:
        val = int(not val)

cap.release()
cv.destroyAllWindows()
