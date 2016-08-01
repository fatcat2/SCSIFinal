# MAIN FILE
import MultiFinder as mf
import TrackedObject as to
import skeleton as skele
import numpy as np
import cv2


def onmouse(event, x, y, flags, param):
    global drag_start
    global isTracking
    global selection
    global frame
    h, w = frame.shape[2]
    if event == cv2.EVENT_LBUTTONDOWN:   # If left mouse button started to be pressed 
        drag_start = (x, y)   # set start of drag region to be mouse's (x, y)
        isTracking = False
        isDragging = True
    elif event == cv2.EVENT_LBUTTONUP:  # left mouse button up indicates end of dragging
        isDragging = False
        drag_start = None
        if selection != None:
            isTracking = True
            print selection
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

if __name__ == "__main__":
    colorList = [((30, 120, 60), (80, 255, 255)), ((74, 80, 80), (114, 230, 230))]#
    averageColors=mf.getAverageColors(colorList)
    trackingItems = {}
    skeleton = skele.Skeleton()
    for i in colorList:
        trackingItems[i] = []
    vidCap = cv2.VideoCapture(0)
    ret, ouput = vidCap.read()
    # imgInit = cv2.cvtColor(imgInit, cv2.COLOR_BGR2HSV)
    # contours = mf.evaluateForContours(imgInit, colorList)
    # last = None
    # if contours is not None and len(contours) > 0:
    #     centers = mf.trimCenters(mf.getCentersAndBoxes(contours), 50)
    #     for c in range(len(centers)):
    #         for j in centers[c]:
    #             x = to.TrackedObject(mf.intTuple(j[1][0]+j[1][1]), j[0], imgInit, colorList[c])
    #             trackingItems[colorList[c]].append(x)
    #             if last is not None:
    #                 pass # skeleton.addLink(x, last)
    #             last = x
    # arm=[None, None, None]
    # print trackingItems
    # for i in trackingItems[colorList[1]]:
    #     if arm[0] is None or i.getCenterPoint()[1]<arm[0].getCenterPoint():
    #         arm[0]=i
    # for i in trackingItems[colorList[1]]:
    #     if i not in arm and \
    #             (arm[1] is None or
    #              mf.distance(i.getCenterPoint(), arm[0].getCenterPoint()) <
    #                      mf.distance(arm[1].getCenterPoint(), arm[0].getCenterPoint())):
    #         arm[1]=i
    # for i in trackingItems[colorList[1]]:
    #     if i not in arm and \
    #             (arm[1] is None or
    #              mf.distance(i.getCenterPoint(), arm[0].getCenterPoint()) <
    #                      mf.distance(arm[1].getCenterPoint(), arm[0].getCenterPoint())):
    #         arm[2] = i
    # print arm
    # if None not in [arm[0], arm[1]]:
    #     skeleton.addLink(arm[0], arm[1])
    # if None not in [arm[1], arm[2]]:
    #     skeleton.addLink(arm[1], arm[2])

    cv2.namedWindow('output')
    cv2.setMouseCallback('output', onmouse)

    #Capture Loop
    while True:
        frame = getNextFrame(vidCap)
        img1 = cv2.cvtColor(vidCap.read()[1], cv2.COLOR_BGR2HSV)
        origImg=np.copy(img1)
        for i in trackingItems.keys():
            for j in trackingItems[i]:
                j.update(origImg)
                cv2.circle(img1, tuple(j.getCenterPoint()), 4, tuple(averageColors[colorList.index(i)]), -1)
                tw=j.getTrackWindow()
                pos=((tw[0], tw[1]), (tw[0]+tw[2], tw[1]+tw[3]))
                cv2.rectangle(img1, pos[0], pos[1], tuple(averageColors[colorList.index(i)]), 3)
                cv2.imshow("debug "+str(i)+str(j), (j.prob&j.maskImage)[::2,::2])
                cv2.moveWindow("debug "+str(i)+str(j), 10*trackingItems.keys().index(i), 0)
        img1=cv2.cvtColor(img1, cv2.COLOR_HSV2BGR)
        skeleton.renderAllLinks(img1)
        cv2.imshow("output", img1[::2, ::2])
        val = cv2.waitKey(10) & 0xFF
        if val == 255:   # No input   (Nothing)
            continue
        if val == 27:    # Escape key (Exit)
            break
    vidCap.release()
    cv2.destroyAllWindows()
