#!/usr/bin/env python

'''
Camshift tracker
================
This is a demo that shows mean-shift based tracking
You select a color objects such as your face and it tracks it.
This reads from video camera (0 by default, or the camera number the user enters)
http://www.robinhewitt.com/research/track/camshift.html
Usage:
------
    camshift.py [<video source>]
    To initialize tracking, select the object with mouse
Keys:
-----
    ESC   - exit
    b     - toggle back-projected probability visualization
'''

import numpy as np
import cv2
class TrackedObject:
    def __init__(self, selc):
        self.area = selc
        print "hello"

    def setTracking(self, isTrack):
        self.isTrack = isTrack

    def setHistogram(self, hist):
        self.hist = hist
selection = None
drag_start = None
isDragging = False
isTracking = False
showBackProj = False
showHistMask = False
frame = None
hist = None

#Ryan's variable additions
trackedObjectList = []


def onmouse(event, x, y, flags, param):
    """Called whenever the mouse does something. It takes in a code describing the event, the location of the event
    in the current window, and other features. If the mouse clicked down, then it starts dragging and stops
    tracking. If the mouse lifts up, then it stops dragging and sets tracking to True. If in between, and the mouse moved
    then it updates the current selection."""
    global drag_start
    global isTracking
    global isDragging
    global selection
    global frame
    h, w = frame.shape[:2]           
    if event == cv2.EVENT_LBUTTONDOWN:   # If left mouse button started to be pressed 
        drag_start = (x, y)   # set start of drag region to be mouse's (x, y)
        isTracking = False
        isDragging = True
    elif event == cv2.EVENT_LBUTTONUP:  # left mouse button up indicates end of dragging
        isDragging = False
        drag_start = None
        temp_trackobj = TrackedObject(selection)
        if selection != None:
            temp_trackobj.setTracking(False)
        trackedObjectList.append(temp_trackobj)
    elif isDragging and event == cv2.EVENT_MOUSEMOVE:    # if currently dragging and mouse is moving
        xo, yo = drag_start              # first compute upperleft anbd lower right
        x0 = max(0, min(xo, x))
        x1 = min(w, max(xo, x))
        y0 = max(0, min(yo, y))
        y1 = min(h, max(yo, y))   # crops to picture size: no out od bounds
        selection = None
        if x1-x0 > 0 and y1-y0 > 0:
            selection = (x0, y0, x1, y1)  # set current drag rectangle




def getNextFrame(vidObj):
    """Takes in the VideoCapture object and reads the next frame, returning one that is half the size 
    (Comment out that line if you want fullsize)."""
    ret, frame = vidObj.read()
    print type(vidObj), type(frame)
    frame = cv2.resize(frame, (0, 0), fx = 0.5, fy = 0.5)
    return frame

#Ryan's addition
def getHSVFromPic():
    blue_sample = cv2.imread("blue_sample.jpg")
    blue_sample = cv2.resize(blue_sample, dsize = (0, 0), fx = 0.5, fy = 0.5)
    h, w, ch = blue_sample.shape
    track_window = (0, 0, w, h)
    hsv_roi = hsv[0:h, 0:w]
    mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
    mask_roi = mask[0:h, 0:w]
    hist = cv2.calcHist(hsv_roi, [0], )


cam = cv2.VideoCapture(1)
ret, frame = cam.read()

cv2.namedWindow('camshift')
cv2.setMouseCallback('camshift', onmouse)
cv2.namedWindow('hist')
cv2.moveWindow('hist', 700, 100)   # Move to reduce overlap

# start processing frames
while True:
    #for the frame
    frame = getNextFrame(cam)
    vis = frame.copy()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    # convert to HSV
    mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))   # eliminate low and high saturation and value values

    #for the object
    # if isDragging and trackedObjectList[0].selection != None:    # if currently dragging and a good region has been selected
    #     x0, y0, x1, y1 = trackedObjectList[0].selection
    #     track_window = (x0, y0, x1-x0, y1-y0)
    #     hsv_roi = hsv[y0:y1, x0:x1]             # access the currently selected region and make a histogram of its hue
    #     mask_roi = mask[y0:y1, x0:x1]
    #     hist = cv2.calcHist( [hsv_roi], [0], mask_roi, [16], [0, 180] )
    #     cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    #     hist = hist.reshape(-1)
    #
    #     vis_roi = vis[y0:y1, x0:x1]          # make the selected region visible
    #     cv2.bitwise_not(vis_roi, vis_roi)
    #     # The next line shows which pixels are being used to make the histogram.
    #     # it sets to black all the ones that are masked away for being too over or under-saturated
    #     if showHistMask:
    #         vis[mask == 0] = 0

    if isTracking:   # If tracking...
        selection = None
        prob = cv2.calcBackProject([hsv], [0], hist, [0, 180], 1)
        prob &= mask
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
        track_box, track_window = cv2.CamShift(prob, track_window, term_crit)

        if showBackProj:
            vis[:] = prob[...,np.newaxis]
        try:
            cv2.ellipse(vis, track_box, (0, 0, 255), 2)
        except:
            print track_box

    cv2.imshow('camshift', vis)

    ch = 0xFF & cv2.waitKey(5)
    if ch == 27:
        break
    elif ch == ord('b'):
        showBackProj = not showBackProj
    elif ch == ord('v'):
        showHistMask = not showHistMask
        
cv2.destroyAllWindows()


