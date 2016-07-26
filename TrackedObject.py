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
    x, y, w, h = 0
    def __init__(self, box, center, image):
        self.tracking_window = box
        x, y, w, h = box
        self.centerpoint = center
        setImage(image)
        self.initHSV()
        # TODO: Set up get hist code to prevent colorshifting over time
    def initHSV(self):
    	maskROI = maskImage[y:y+h, x:x+w]
    	hsvROI = hsvImage[y:y+h, x:x+w]
    	self.setHist(cv2.calcHist([hsvROI], [0], maskROI, [64], [0, 255]))
        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX) #reduces the extremes
        hist = hist.reshape(-1)	
    	
        # Getters and Setters
    def setHist(self, hist):
        self.hist = hist
    def setImage(self, hsvImage):
    	self.maskImage = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
    	self.hsvImage = hsvImage
    	self.maskImage()
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
    def getTrackBox(self):
    	return track_box
    def updateObk(self, coords):
        self.centerpoint = coords

    def update(self, image):
    	setImage(image)
    	prob = cv2.calcBackProject([hsv], [0], hist, [0, 180], 1)
    	prob &= maskImage
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 ) #criteria for termination
        track_box, track_window = cv2.CamShift(prob, track_window, term_crit)
        pass
        # TODO: Add code for Camshift