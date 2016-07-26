import cv2
import numpy as np
class TrackedObject:
    hist = None
    tracking_window = None
    centerpoint = (0, 0)
    hsvImage = None
    maskImage = None
    hsvROI = None
    x, y, w, h = 0
    def __init__(self, box, center, image):
        self.tracking_window = box
        x, y, w, h = box
        self.centerpoint = center
        self.hsvImage = image
        # TODO: Set up get hist code to prevent colorshifting over time
    def initHSV(self):
    	maskImage = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
    	maskROI = maskImage[y:y+h, x:x+w]
    	hsvROI = hsvImage[y:y+h, x:x+w]
    	self.setHist(cv2.calcHist([hsvROI], [0], maskROI, [64], [0, 255]))
    	
        # Getters and Setters
    def setHist(self, hist):
        self.hist = hist
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
    def updateObk(self, coords):
        self.centerpoint = coords

    def update(self, image):
        pass
        # TODO: Add code for Camshift