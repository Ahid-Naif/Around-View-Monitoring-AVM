import cv2
import numpy as np
from myPackage.UndistortFisheye import UndistortFisheye

undistortFisheye = UndistortFisheye()

video = cv2.VideoCapture(1)

while True:
    isGrabbed, frame = video.read()

    clearImage = undistortFisheye.undistort(frame)

    cv2.imshow("Undistorted", clearImage)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
