import cv2
import numpy as np


class TrackedObject:
    hist = None
    tracking_window = None
    track_box = None
    centerpoint = (0, 0)
    hsvImage = None
    maskImage = None
    hsvROI = None
    prob = None
    x, y, w, h = 0, 0, 0, 0

    def __init__(self, box, center, image):
        self.tracking_window = box
        x, y, w, h = box[0]+box[1]
        self.centerpoint = center
        self.setImage(image)
        self.initHSV()
        # TODO: Set up get hist code to prevent colorshifting over time

    def initHSV(self):
        self.maskROI = self.maskImage[self.y:self.y + self.h, self.x:self.x + self.w]
        self.hsvROI = self.hsvImage[self.y:self.y + self.h, self.x:self.x + self.w]
        self.setHist(cv2.calcHist([self.hsvROI], [0], self.maskROI, [64], [0, 255]))
        cv2.normalize(self.hist, self.hist, 0, 255, cv2.NORM_MINMAX)  # reduces the extremes
        self.hist = self.hist.reshape(-1)

        # Getters and Setters

    def setHist(self, hist):
        self.hist = hist

    def setImage(self, hsvImage):
        self.hsvImage = hsvImage
        self.maskImage = cv2.inRange(hsvImage, np.array((0., 60., 32.)), np.array((180., 255., 255.)))

    def setTrackingWindow(self, trackwindow):
        self.tracking_window = trackwindow

    def setCenterPoint(self, cp):
        self.centerpoint = cp

    def getHist(self):
        return self.hist

    def getTrackWindow(self):
        return self.tracking_window

    def getCenterPoint(self):
        return self.centerpoint

    def getProbability(self):
        return self.prob

    def getTrackBox(self):
        return self.track_box

    def updateObk(self, coords):
        self.centerpoint = coords

    def update(self, image):
        self.setImage(image)
        self.prob = cv2.calcBackProject([self.hsvImage], [0], self.hist, [0, 180], 1)
        # print self.prob.shape
        self.prob &= self.maskImage
        print self.tracking_window.shape
        cv2.imshow("prob", self.prob)
        cv2.waitKey(0)
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )  # criteria for termination
        self.track_box, self.tracking_window = cv2.CamShift(self.prob, self.tracking_window, term_crit)
        # TODO: Add code for Camshift