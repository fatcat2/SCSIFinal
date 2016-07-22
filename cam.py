import numpy as np
import cv2

cam = cv2.VideoCapture(1)
ret, frame = cam.read()
for x in 5000:
    vis = frame.copy()
    cv2.imshow('camshift', vis)
cv2.destroyAllWindows()