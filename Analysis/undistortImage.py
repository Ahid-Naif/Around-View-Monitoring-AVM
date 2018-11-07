import cv2
import numpy as np
from myPackage.UndistortFisheye import UndistortFisheye
from myPackage.customizedTrackBar import customizedTrackBar
import glob

# balanceTrackBar = customizedTrackBar(0, 0.1, 1, 0, "balance", "Tuning")

undistortFisheye = UndistortFisheye()

while True:
    image = cv2.imread("raw.jpg")

    # balance = balanceTrackBar.getValue()

    clearImage1 = undistortFisheye.undistort(image)
    clearImage3 = undistortFisheye.undistort3(image)

    # clearImages = np.hstack((clearImage1, clearImage2))
    cv2.imshow("Undistorted", clearImage1)
    cv2.imshow("Undistorted3", clearImage3)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord("r"):
        undistortFisheye.reset()

cv2.destroyAllWindows()
