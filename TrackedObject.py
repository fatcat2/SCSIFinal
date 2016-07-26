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
        x, y, w, h = box
        self.centerpoint = center
        self.setImage(image)
        self.initHSV()
        # TODO: Set up get hist code to prevent colorshifting over time

    def initHSV(self):
        self.maskROI = maskImage[y:y + h, x:x + w]
        self.hsvROI = hsvImage[y:y + h, x:x + w]
        self.setHist(cv2.calcHist([hsvROI], [0], maskROI, [64], [0, 255]))
        cv2.normalize(hist, hist, 0, 255, cv2.normalize_MINMAX)  # reduces the extremes
        self.hist = hist.reshape(-1)

        # Getters and Setters

    def setHist(self, hist):
        self.hist = hist

    def setImage(self, hsvImage):
        self.hsvImage = hsvImage
        self.maskImage = cv2.inRange(hsvImage, np.array((0., 60., 32.)), np.array((180., 255., 255.)))

    def setTrackingWindow(self, trackwindow):
        self.tracking_window = trackingwindow

    def setCenterPoint(self, cp):
        self.centerpoint = cp

    def getHist(self):
        return hist

    def getTrackWindow(self):
        return tracking_window

    def getCenterPoint(self):
        return centerpoint

    def getProbability(self):
        return prob

    def getTrackBox(self):
        return track_box

    def updateObk(self, coords):
        self.centerpoint = coords

    def update(self, image):
        setImage(image)
        self.prob = cv2.calcBackProject([hsv], [0], hist, [0, 180], 1)
        self.prob &= self.maskImage
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )  # criteria for termination
        self.track_box, self.track_window = cv2.CamShift(prob, track_window, term_crit)
        # TODO: Add code for Camshift