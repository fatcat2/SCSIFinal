import cv2
import numpy as np
import tracking_functions as tf
DEBUG = True
def show_hist(hist, thin):
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

    # ----- Variables -----
    hist = None
    tracking_window = None
    track_box = None
    centerPoint = (0, 0)
    hsvImage = None
    maskImage = None
    maskROI = None
    hsvROI = None
    prob = None
    term_crit = None
    x, y, w, h = 0, 0, 0, 0

    # ----- Setup functions -----

    def __init__(self, box, center, image, color_range):
        self.tracking_window = box
        self.x, self.y, self.w, self.h = box
        self.centerPoint = center
        self.colRng = color_range  # Range of colors used to generate TrackedObject
        self.setImage(image)
        self.initHSV()
        self.term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)  # criteria for termination

    def initHSV(self):
        col_img = cv2.inRange(self.hsvImage, self.colRng[0], self.colRng[1])
        self.maskROI = self.maskImage[self.y:self.y + self.h, self.x:self.x + self.w]
        self.hsvROI = (self.hsvImage &
                       cv2.merge((col_img, col_img, col_img))
                       )[self.y:self.y + self.h, self.x:self.x + self.w]
        if DEBUG:
            cv2.imshow("Showimage "+str(self), cv2.cvtColor(self.hsvImage & cv2.merge((col_img, col_img, col_img)), cv2.COLOR_HSV2BGR))
        self.setHist(cv2.calcHist([self.hsvROI], [0], self.maskROI, [32], [0, 180]))
        if DEBUG:
            cv2.waitKey(0)
        cv2.normalize(self.hist, self.hist, 0, 255, cv2.NORM_MINMAX)  # reduces the extremes
        self.hist = self.hist.reshape(-1)

    # ----- Setters -----

    def setHist(self, hist):
        if DEBUG:
            show_hist(hist, str(self))
        self.hist = hist
        self.hist[0] = 0  # Remove red derived from black areas
        # TODO: improve this removal- right now, it can block true red

    def setImage(self, hsv_image):
        self.hsvImage = hsv_image
        self.maskImage = cv2.inRange(hsv_image, np.array((0., 60., 32.*2)), np.array((180., 255., 255.)))

    def setTrackingWindow(self, tracking_window):
        self.tracking_window = tracking_window

    def setCenterPoint(self, cp):
        self.centerPoint = cp

    # ----- Getters -----

    def getHist(self):
        return self.hist

    def getTrackingWindow(self):
        return self.tracking_window

    def getCenterPoint(self):
        return self.centerPoint

    def getProbability(self):
        return self.prob

    def getTrackBox(self):
        return self.track_box

    # ----- Update Functions -----

    def updateCenter(self):
        center = (self.tracking_window[0]+self.tracking_window[2]/2,
                  self.tracking_window[1]+self.tracking_window[3]/2)
        center = tf.intTuple(center)
        self.setCenterPoint(center)

    def update(self, image):
        new_img = image  # Prevent modification of image
        self.setImage(cv2.blur(new_img, (5, 5)))
        self.prob = cv2.calcBackProject([self.hsvImage], [0], self.hist, [0, 180], 1)
        self.prob &= self.maskImage
        self.track_box, self.tracking_window = cv2.CamShift(self.prob, self.tracking_window, self.term_crit)
        self.updateCenter()