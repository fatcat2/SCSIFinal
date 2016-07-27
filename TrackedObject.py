import cv2
import numpy as np
import MultiFinder as mf



class TrackedObject:
    hist = None
    tracking_window = None
    track_box = None
    centerpoint = (0, 0)
    hsvImage = None
    maskImage = None
    hsvROI = None
    prob = None
    term_crit = None
    x, y, w, h = 0, 0, 0, 0

    def __init__(self, box, center, image):
        self.tracking_window = box
        self.x, self.y, self.w, self.h = box
        self.centerpoint = center

        self.setImage(image)
        self.initHSV()
        self.term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)  # criteria for termination
        # TODO: Set up get hist code to prevent colorshifting over time

    def initHSV(self):
        self.maskROI = self.maskImage[self.y:self.y + self.h, self.x:self.x + self.w]
        self.hsvROI = self.hsvImage[self.y:self.y + self.h, self.x:self.x + self.w]
        self.setHist(cv2.calcHist([self.hsvROI], [0], self.maskROI, [64], [0, 180]))
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

    def updateCenter(self):
        center = (self.tracking_window[0]+self.tracking_window[2]/2,
                  self.tracking_window[1]+self.tracking_window[3]/2)
        #center = self.track_box[0]
        center=mf.intTuple(center)
        self.setCenterPoint(center)


    def update(self, image):
        nImg=image
        self.setImage(cv2.blur(nImg, (5,5)))
        self.prob = cv2.calcBackProject([self.hsvImage], [0], self.hist, [0, 180], 1)
        self.prob &= self.maskImage
        self.track_box, self.tracking_window = cv2.CamShift(self.prob, self.tracking_window, self.term_crit)
        self.updateCenter()
        # TODO: Add code for Camshift