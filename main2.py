# MAIN FILE
import MultiFinder as mf
import TrackedObject as to
import skeleton as skele
import numpy as np
import cv2
import TrackedObject as to

selection = None
drag_start = None
isDragging = False
isTracking = False
showBackProj = False
showHistMask = False
frame = None
hist = None
trackedObjectList = []

def onmouse(event, x, y, flags, param):
    global drag_start
    global isTracking
    global isDragging
    global selection
    global frame
    h, w = frame.shape[:2]           
    if event == cv2.EVENT_LBUTTONDOWN:
        drag_start = (x, y)
        isTracking = False
        isDragging = True
    elif event == cv2.EVENT_LBUTTONUP:  # left mouse button up indicates end of dragging
        isDragging = False
        drag_start = None
        if selection != None:
            isTracking = True
            # print selection
    elif isDragging and event == cv2.EVENT_MOUSEMOVE:    # if currently dragging and mouse is moving
        xo, yo = drag_start              # first compute upperleft anbd lower right
        x0 = max(0, min(xo, x))
        x1 = min(w, max(xo, x))
        y0 = max(0, min(yo, y))
        y1 = min(h, max(yo, y))   # crops to picture size: no out od bounds
        selection = None
        if x1-x0 > 0 and y1-y0 > 0:
            selection = (x0, y0, x1, y1)  # set current drag rectangle


def show_hist(hist):
     """Takes in the histogram, and displays it in the hist window."""
     bin_count = hist.shape[0]
     bin_w = 24
     img = np.zeros((256, bin_count*bin_w, 3), np.uint8)
     for i in xrange(bin_count):
         h = int(hist[i])
         cv2.rectangle(img, (i*bin_w+2, 255), ((i+1)*bin_w-2, 255-h), (int(180.0*i/bin_count), 255, 255), -1)
     img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
     cv2.imshow('hist', img)

def getNextFrame(vidObj):
    """Takes in the VideoCapture object and reads the next frame, returning one that is half the size 
    (Comment out that line if you want fullsize)."""
    ret, frame = vidObj.read()
    # print type(vidObj), type(frame)
    frame = cv2.resize(frame, (0, 0), fx = 0.5, fy = 0.5)
    return frame

#create the camera boject
cam = cv2.VideoCapture(0)
ret, frame = cam.read() #return boolean retval and the image obtained by the camera
frame = cv2.resize(frame, dsize = (0, 0), fx = 0.5, fy = 0.5) #resizes the image in half to be more manageable

#moving and naming windows to reduce overlap
cv2.namedWindow('camshift')
cv2.setMouseCallback('camshift', onmouse)
cv2.namedWindow('hist')
cv2.moveWindow('hist', 700, 100)   # Move to reduce overlap

# start processing frames
while True:
    frame = getNextFrame(cam)
    vis = frame.copy()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    # convert to HSV
    mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))   # eliminate low and high saturation and value values

    if isDragging and selection != None:    # if currently dragging and a good region has been selected
        x = to.TrackedObject(coords, hsv, mask)
        trackedObjectList.append(x)
        x0, y0, x1, y1 = selection
        track_window = (x0, y0, x1-x0, y1-y0) #(origin x, origin y, width, height)
        hsv_roi = hsv[y0:y1, x0:x1]             # access the currently selected region and make a histogram of its hue 
        mask_roi = mask[y0:y1, x0:x1]
        hist = cv2.calcHist([hsv_roi], [0], mask_roi, [64], [0, 255]) #takes in the ROI of the HSV image, the blue channel, the ROI mask, range of colors, and the range
        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX) #reduces the extremes
        hist = hist.reshape(-1)
        show_hist(hist)



        vis_roi = vis[y0:y1, x0:x1]
        cv2.bitwise_not(vis_roi, vis_roi)
        if showHistMask:
            vis[mask == 0] = 0



        for obj in trackedObjectList:  # If tracking...
            # selection = None #clear the selection
            prob = cv2.calcBackProject([hsv], [0], hist, [0, 180], 1) #calculates the probability of similarity
            prob &= mask #adds the probability of hit rate to the mask
            #count gets rid after a certain count if it can't settle
            term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 ) #criteria for termination
            track_box, track_window = cv2.CamShift(prob, track_window, term_crit) #returns a box for the ellipse to use and box parameters to be used as a search box

            if showBackProj:
                vis[:] = prob[...,np.newaxis]
            try:
                cv2.ellipse(vis, track_box, (0, 0, 255), 2) #draws the red ellipse with a stroke of 2 onto the copy of the frame, and uses the dimensions of the track_box variable
            except:
                # print track_box
    cv2.imshow('camshift', vis)

    ch = 0xFF & cv2.waitKey(5)
    if ch == 27:
        break
    elif ch == ord('b'):
        showBackProj = not showBackProj
    elif ch == ord('v'):
        showHistMask = not showHistMask
        
cv2.destroyAllWindows()