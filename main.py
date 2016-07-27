# MAIN FILE
import MultiFinder as mf
import TrackedObject as to
import skeleton as skele
import numpy as np
import cv2
if __name__ == "__main__":
    colorList = [((30, 120, 60), (80, 255, 255)), ((100, 120, 60), (140, 255, 255)), ]#
    averageColors=mf.getAverageColors(colorList)
    trackingItems = {}
    skeleton = skele.Skeleton()
    for i in colorList:
        trackingItems[i] = []
    vidCap = cv2.VideoCapture(1)
    ret, imgInit = vidCap.read()
    imgInit = cv2.cvtColor(imgInit, cv2.COLOR_BGR2HSV)
    contours = mf.evaluateForContours(imgInit, colorList)
    last = None
    if contours is not None and len(contours) > 0:
        centers = mf.getCentersAndBoxes(contours)
        for c in range(len(centers)):
            for j in centers[c]:
                x = to.TrackedObject(mf.intTuple(j[1][0]+j[1][1]), j[0], imgInit)
                trackingItems[colorList[c]].append(x)
                if last is not None:
                    skeleton.addLink(x, last)
                last = x

    while True:
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
                cv2.moveWindow("debug "+str(i)+str(j), j.prob.shape[1]/2*trackingItems.keys().index(i), 0)
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
