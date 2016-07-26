# MAIN FILE
import MultiFinder as mf
import TrackedObject as to
import numpy as np
import cv2
if __name__ == "__main__":
    colorList = [((40, 120, 60), (80, 255, 255)), ((100, 120, 60), (140, 255, 255))]
    averageColors=mf.getAverageColors(colorList)
    trackingItems = {}
    for i in colorList:
        trackingItems[i] = []
    vidCap = cv2.VideoCapture(0)
    #take in initial image to determine objects to track
    ret, imgInit = vidCap.read()
    imgInit = cv2.cvtColor(imgInit, cv2.COLOR_BGR2HSV)
    cv2.imshow("Test", imgInit)
    cv2.waitKey(0)
    contours = mf.evaluateForContours(imgInit, colorList)
    if contours is not None and len(contours) > 0:
        centers = mf.getCentersAndBoxes(contours)
        for c in range(len(centers)):
            for j in centers[c]:
                x = to.TrackedObject(j[1], j[0])
                trackingItems[colorList[c]].append(x)
    while True:
        ret, img1 = vidCap.read()
        for i in trackingItems.keys():
            for j in trackingItems[i]:
                j.update(img1)
                cv2.circle(img1, j.getCenter(), 4, averageColors[colorList.index(i)], -1)
        cv2.imshow("output", img1)
        val = cv2.waitKey(10) & 0xFF
        if val == 255:   # No input   (Nothing)
            continue
        if val == 27:    # Escape key (Exit)
            break
    vidCap.release()
    cv2.destroyAllWindows()
