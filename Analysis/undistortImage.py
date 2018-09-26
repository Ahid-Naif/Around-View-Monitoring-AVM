import cv2
import numpy as np
from myPackage.UndistortFisheye import UndistortFisheye
import glob

def doNothing(_):
    pass
cv2.namedWindow("Undistorted")
cv2.createTrackbar("balance", "Undistorted", 0, 100, doNothing)

undistortFisheye = UndistortFisheye()

while True:
    image = cv2.imread("dataset/Calibration/image_no_4.jpg")

    balance = cv2.getTrackbarPos("balance", "Undistorted")/100
    clearImage1 = undistortFisheye.undistort(image)
    clearImage2 = undistortFisheye.undistort2(image, balance=balance)
    clearImage3 = undistortFisheye.calibrate(image, balance=balance)

    clearImages = np.hstack((clearImage2, clearImage3))
    cv2.imshow("Undistorted", clearImages)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
