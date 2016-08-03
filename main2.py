# MAIN FILE Hello
import MultiFinder as mf
import TrackedObject as to
import skeleton as sk
import numpy as np
import cv2

selection = None
drag_start = None
conn_start = None
isDragging = False
isTracking = False
isLinking = False
frame = None
hist = None
maxDistance = 900
trackedObjectList = []
mrSkeletal = sk.MidpointSkeleton()


def onmouse(event, x, y, flags, param):
    global drag_start
    global conn_start
    global isTracking
    global isDragging
    global isLinking
    global selection
    global frame
    global mrSkeletal
    global trackedObjectList
    global maxDistance
    h, w = frame.shape[:2]
    if event == cv2.EVENT_LBUTTONDOWN:
        #print "MOUSEDOWN"
        drag_start = (x, y)
        isTracking = False
        isDragging = True
    elif event == cv2.EVENT_LBUTTONUP:  # left mouse button up indicates end of dragging
        #print "MOUSEUP"
        isDragging = False
        drag_start = None
        if selection != None:
            isTracking = True
            # print selection
    elif isDragging and event == cv2.EVENT_MOUSEMOVE:    # if currently dragging and mouse is moving
        #print "MOUSEMOVE"
        xo, yo = drag_start              # first compute upperleft anbd lower right
        x0 = max(0, min(xo, x))
        x1 = min(w, max(xo, x))
        y0 = max(0, min(yo, y))
        y1 = min(h, max(yo, y))   # crops to picture size: no out od bounds
        selection = None
        if x1-x0 > 0 and y1-y0 > 0:
            selection = (x0, y0, x1, y1)  # set current drag rectangle
    elif event == cv2.EVENT_RBUTTONDOWN:
        point = (x, y)
        for currCheck in trackedObjectList:
            if mf.distance(point, currCheck.getCenterPoint()) < maxDistance:
                if isLinking:
                    link = conn_start, currCheck
                    if not (conn_start is currCheck or mrSkeletal.contains(link) or mrSkeletal.contains(link[::-1])):
                        mrSkeletal.addLink(link[0], link[1])
                    isLinking = not isLinking
                else:
                    conn_start = currCheck
                    isLinking = not isLinking
                break


def show_hist(histogram):
    """Takes in the histogram, and displays it in the hist window."""
    bin_count = histogram.shape[0]
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
    ret, outframe = vidObj.read()
    # print type(vidObj), type(frame)
    outframe = cv2.resize(outframe, dsize=(0, 0), fx=0.5, fy=0.5)
    return outframe

#create the camera boject
cam = cv2.VideoCapture(1)
ret, frame = cam.read()  # return boolean retval and the image obtained by the camera
frame = cv2.resize(frame, dsize=(0, 0), fx = 0.5, fy = 0.5)  # resizes the image in half to be more manageable
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
print frame.shape
#shape = [frame.shape[0]*2]+[frame.shape[1]]
writ = cv2.VideoWriter("Vid1.avi", fourcc, 25.0, frame.shape[:2][::-1], 1)

#moving and naming windows to reduce overlap
cv2.namedWindow('camshift')
cv2.setMouseCallback('camshift', onmouse)
cv2.namedWindow('hist')
cv2.moveWindow('hist', 700, 100)   # Move to reduce overlap

# start processing frames
for i in range(2000):
    # print i
    frame = getNextFrame(cam)
    vis = frame.copy()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    # convert to HSV
    mask = cv2.inRange(hsv, np.array((0., 0., 32.)), np.array((180., 255., 255.)))   # Eliminate low and high saturation and value values

    if isDragging and selection is not None:    # if currently dragging and a good region has been selected
        x0, y0, x1, y1 = selection
        track_window = (x0, y0, x1-x0, y1-y0)
        hsv_roi = hsv[y0:y1, x0:x1]             # access the currently selected region and make a histogram of its hue
        mask_roi = mask[y0:y1, x0:x1]
        hist = cv2.calcHist( [hsv_roi], [0], mask_roi, [16], [0, 180] )
        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
        hist = hist.reshape(-1)
        show_hist(hist)

    if not isDragging and selection is not None:
        x0, y0, x1, y1 = selection
        x = to.TrackedObject((x0, y0, x1, y1), hsv, mask, hist)
        trackedObjectList.append(x)
        selection = None
        show_hist(hist)
    black = np.zeros(frame.shape)
    for obj in trackedObjectList:  # If tracking...
        obj.update(hsv)
        cv2.circle(vis, obj.getCenterPoint(), 8, (0, 0, 255), 2)
        cv2.circle(vis, obj.getCenterPoint(), 30, (125, 255, 125), 1)
    mrSkeletal.renderAllLinks(black)
    mrSkeletal.renderAllLinks(vis)
    cv2.imshow('Skeleton', black)
    cv2.imshow('camshift', vis)
    #out = np.concatenate((vis, black), axis=1)
    print vis.shape
    cv2.imshow("vid", vis)
    writ.write(vis)
    if trackedObjectList:
        cv2.imshow('prob1', trackedObjectList[0].prob)

    ch = 0xFF & cv2.waitKey(5)
    if ch == 27:
        break
writ.release()
cv2.destroyAllWindows()