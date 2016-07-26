class TrackedObject:
    hist = None
    tracking_window = None
    centerpoint = (0, 0)

    def __init__(self, box, center):
        self.tracking_window = box
        self.centerpoint = center
        # TODO: Set up get hist code to prevent colorshifting over time

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