import cv2
import numpy as np
import MultiFinder as mf

def show_hist(hist,thin):
     """Takes in the histogram, and displays it in the hist window."""
     bin_count = hist.shape[0]
     bin_w = 24
     img = np.zeros((256, bin_count*bin_w, 3), np.uint8)
     for i in xrange(bin_count):
         h = int(hist[i])
         cv2.rectangle(img, (i*bin_w+2, 255), ((i+1)*bin_w-2, 255-h), (int(180.0*i/bin_count), 255, 255), -1)
     img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
     cv2.imshow(thin, img)

class TrackedObject:
    hist = None
    track_window = None
    track_box = None
    centerpoint = (0, 0)
    hsvImage = None
    maskImage = None
    hsvROI = None
    prob = None
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    x, y, w, h = 0, 0, 0, 0
    isTracking = False

    def __init__(self, coords, image, mask, hist):
        x0, y0, x1, y1 =  coords
        self.track_window = (x0, y0, x1-x0, y1-y0)

        self.setImage(image)
        self.setMask(mask)
        self.hist = hist

    def initHSV(self):
        self.maskROI = self.maskImage[self.y:self.y + self.h, self.x:self.x + self.w]
        self.hsvROI = self.hsvImage[self.y:self.y + self.h, self.x:self.x + self.w]
        self.setHist(cv2.calcHist([self.hsvROI], [0], self.maskROI, [32], [0, 180]))
        cv2.normalize(self.hist, self.hist, 0, 255, cv2.NORM_MINMAX)  # reduces the extremes
        self.hist.reshape(-1)

        # Getters and Setters

    def setHist(self, hist):
        show_hist(hist, str(self))
        self.hist = hist
        self.hist[0] = 0

    def setImage(self, hsvImage):
        self.hsvImage = hsvImage
        self.maskImage = cv2.inRange(hsvImage, np.array((0., 60., 32.*2)), np.array((180., 255., 255.)))

    def setTrackingWindow(self, trackwindow):
        self.track_window = trackwindow

    def setCenterPoint(self, cp):
        self.centerpoint = cp
    def setTrackBox(self, track_box):
        self.track_box = track_boxd
    def isTracking(self):
        return self.isTracking

    def getHist(self):
        return self.hist

    def getTrackWindow(self):
        return self.track_window

    def getCenterPoint(self):
        return self.centerpoint

    def getProbability(self):
        return self.prob

    def setMask(self, m):
        self.maskImage = m  

    def getTrackBox(self):
        return self.track_box

    def updateObk(self, coords):
        self.centerpoint = coords

    def getImage(self):
        return self.hsvImage

    def getMask(self):
        return self.maskImage
    
    def setHist(self, hist):
        self.hist = hist

    def updateCenter(self):
        center = (self.track_window[0]+self.track_window[2]/2,
                  self.track_window[1]+self.track_window[3]/2)
        center=mf.intTuple(center)
        self.setCenterPoint(center)


    def update(self, image):
        nImg=image
        self.setImage(nImg)
        self.prob = cv2.calcBackProject([self.hsvImage], [0], self.hist, [0, 180], 1)
        cv2.imshow(":l",self.prob)
        self.prob &= self.maskImage
        self.track_box, self.track_window = cv2.CamShift(self.prob, tuple(self.track_window), self.term_crit)
        self.updateCenter() 