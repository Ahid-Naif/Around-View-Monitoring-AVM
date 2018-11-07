import cv2
import numpy as np
from myPackage.UndistortFisheye import UndistortFisheye
from PerspectiveTransformation.EagleView import EagleView

video = cv2.VideoCapture(0)

undistortFisheye = UndistortFisheye()
eagleView = EagleView()
eagleView.setDimensions((210, 108), (425, 115), (587, 345), (44, 335))

while True:
    isGrabbed, frame = video.read()
    if not isGrabbed:
        break

    clearImage1 = undistortFisheye.undistort(frame)
    topDown = eagleView.transfrom(clearImage1)
    cv2.imshow("Bird's Eye View", topDown)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break   

cv2.destroyAllWindows()
