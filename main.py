#MAIN FILE
import MultiFinder as mf
import TrackedObject as to
import numpy as np
import cv2
if __name__ == "__main__":
	TrackedObjectList = []
	vidCap = cv2.VideoCapture(0)
	#take in initial image to determine objects to track
	ret,imgInit = vidCap.read()
	imgInit = cv2.cvtColor(imgInit, cv2.COLOR_BGR2HSV)
	contours = mf.evaluateForContours(imgInit, [[(40, 120, 60), (80, 255, 255)], [(100, 120, 60), (140, 255, 255)]])
	if contours is not None and len(contours) > 0:
			centers = getCentersAndBoxes(contours)
			for c in centers:
				x = to.TrackedObject(c[1], c[0])
				TrackedObjectList.append(x)
				print x
	while True:
		ret, img1 = vidCap.read()
		cv2.imshow("output", img1)
		val = cv2.waitKey(10) & 0xFF
		if val == 255:   # No input   (Nothing)
		    continue
		if val == 27:    # Escape key (Exit)
		    break
	vidCap.release()
	cv2.destroyAllWindows()
