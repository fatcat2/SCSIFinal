#MAIN FILE
import MultiFinder as mf
import TrackedObject as to
import numpy as np
import cv2
if __name__ == "__main__":
	vidCap = cv2.VideoCapture(0)
	ret,imgInit = vidCap.read()
	
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
