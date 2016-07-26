from Carbon.QuickTime import kGraphicsExportGetColorSyncProfileSelect
import colorsys
import cv2
import numpy

def trimToRange(image, low=[0, 0, 0], high=[180, 255, 255]):
    """Accepts an image and two HSV tuples. The first must have all values lower than the second.
    Sets all pixels in the image with higher H,S, and V values then the first and lower than the second to white and all
     other pixels to black. Returns the modified image.
    """
    lowv, highv = numpy.array(low), numpy.array(high)
    return cv2.inRange(image, lowv, highv)

def prepImage(image):
    """Default function for the evaluateForContours function.
    Accepts and returns an image.
    Opens and then closes the image, using a kernel of a 17x17 ellipse.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17))
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return image


def evaluateForContours(image, HSVRanges, morphing=prepImage):
    """Accepts an image, a list of pairs of HSV tuples, each pair defining a range of values,
    and an optional processing function. It passes the image and each range to the trimToRange function
    It then applies the function, then finds all the contours.
    It returns a list containing a list for each range that contains all the contours for that range.
    """
    out=[]
    for i in HSVRanges:
        newImage = image
        grayImg = trimToRange(newImage, i[0], i[1])
        grayImg = morphing(grayImg)
        im2, contours, hier = cv2.findContours(grayImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        out.append(contours)
    return out

def getCentersAndBoxes(contours):
    """Accepts a list of lists of contours, each sublist belonging to a specific color.
    It then determines the center of each contour by constructing the minimum area rectangle,
        then averaging the corners.
    Returns a list containing a list for each color, which holds pairs of center points and rotatedRects.
    """
    out = []
    for i in contours:
        o2=[]
        for j in i:
            corners = cv2.boxPoints(cv2.minAreaRect(j))  # Get minimum area rectangle, then gets the points
            o2.append([[int(numpy.sum(corners[:, 0])/4), int(numpy.sum(corners[:, 1])/4)], cv2.minAreaRect(j)])
        out.append(o2)
    return out


def HSV2BGR(color):
    print color, numpy.array(colorsys.hsv_to_rgb(color[0]/180, color[1]/255, color[2]/255)[::-1])*255
    return (numpy.array(colorsys.hsv_to_rgb(color[0]/180, color[1]/255, color[2]/255)[::-1])*255).tolist()


if __name__ == "__main__":
    vidCap = cv2.VideoCapture(-1)
    ranges = [[(40,  120, 60),  (80, 255, 255)],
              [(100, 120, 60),  (140, 255, 255)],
              [(20,  120, 60),  (40, 255, 255)],
              [(130, 120, 60),  (170, 255, 255)]]
    colors = []
    for c in ranges:
        colors.append(HSV2BGR(numpy.mean(numpy.array(c), axis=0).tolist()))
    pastCenters = []
=======
if __name__=="__main__":
    vidCap = cv2.VideoCapture(0)    
>>>>>>> origin/master
    while True:
        ret, img1 = vidCap.read()
        origImg = img1
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        contours = evaluateForContours(img1, ranges)
        #img2 = numpy.zeros(img1.shape, numpy.uint8)
        img2 = origImg#prepImage(origImg)
        if contours is not None and len(contours) > 0:
            centers = getCentersAndBoxes(contours)
            for c in range(len(centers)):
                for j in centers[c]:
                    pastCenters.append([j[0], colors[c]])
        for c in pastCenters:
            cv2.circle(img2, tuple(c[0]), 20, c[1], -1)

        null = numpy.zeros(img1.shape[0:2], numpy.uint8)
        newsize = tuple(numpy.array(img1.shape[0:2][::-1])/2)
        img2=cv2.resize(img2,newsize)
        cv2.imshow("output", img2)
        val = cv2.waitKey(10) & 0xFF
        if val == 255:   # No input   (Nothing)
            continue
        if val == 27:    # Escape key (Exit)
            break

    vidCap.release()
    cv2.destroyAllWindows()