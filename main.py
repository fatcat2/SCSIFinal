# MAIN FILE
import tracking_functions as tf
import TrackedObject as to
import skeleton
import numpy as np
import cv2
if __name__ == "__main__":
    colorList = [((30, 120, 60), (80, 255, 255)), ((74, 80, 80), (114, 230, 230))]#
    averageColors=tf.getAverageColors(colorList)
    trackingItems = {}
    animationSkeleton = skeleton.Skeleton()
    for i in colorList:
        trackingItems[i] = []
    vidCap = cv2.VideoCapture(0)
    ret, imgInit = vidCap.read()
    imgInit = cv2.cvtColor(imgInit, cv2.COLOR_BGR2HSV)
    contours = tf.evaluateForContours(imgInit, colorList)
    last = None
    if contours is not None and len(contours) > 0:
        centers = tf.trimCenters(tf.getCentersAndBoxes(contours), 50)
        for c in range(len(centers)):
            for j in centers[c]:
                x = to.TrackedObject(tf.intTuple(j[1][0]+j[1][1]), j[0], imgInit, colorList[c])
                trackingItems[colorList[c]].append(x)
                if last is not None:
                    pass # skeleton.addLink(x, last)
                last = x
    arm = [None, None, None]
    print trackingItems
    for i in trackingItems[colorList[1]]:
        if arm[0] is None or i.getCenterPoint()[1]<arm[0].getCenterPoint():
            arm[0]=i
    for i in trackingItems[colorList[1]]:
        if i not in arm and \
                (arm[1] is None or
                 tf.distance(i.getCenterPoint(), arm[0].getCenterPoint()) <
                         tf.distance(arm[1].getCenterPoint(), arm[0].getCenterPoint())):
            arm[1]=i
    for i in trackingItems[colorList[1]]:
        if i not in arm and \
                (arm[1] is None or
                 tf.distance(i.getCenterPoint(), arm[0].getCenterPoint()) <
                         tf.distance(arm[1].getCenterPoint(), arm[0].getCenterPoint())):
            arm[2] = i
    print arm
    if None not in [arm[0], arm[1]]:
        skeleton.addLink(arm[0], arm[1])
    if None not in [arm[1], arm[2]]:
        skeleton.addLink(arm[1], arm[2])

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
