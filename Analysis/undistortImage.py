import cv2
import numpy as np
from myPackage.UndistortFisheye import UndistortFisheye
from myPackage.myTrackBar import customizedTrackBar
import glob

balanceTrackBar = customizedTrackBar(0, 0.1, 1, 0, "balance", "Tuning")

undistortFisheye = UndistortFisheye()

while True:
    image = cv2.imread("RawImage2.jpg")

    balance = balanceTrackBar.getValue()

    clearImage1 = undistortFisheye.undistort(image)
    clearImage2 = undistortFisheye.undistort2(image, balance=balance)

    clearImages = np.hstack((clearImage1, clearImage2))
    cv2.imshow("Undistorted", clearImages)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
