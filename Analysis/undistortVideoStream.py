import cv2
import numpy as np
from myPackage.UndistortFisheye import UndistortFisheye
import glob

def doNothing(_):
    pass
cv2.namedWindow("Undistorted")
cv2.createTrackbar("balance", "Undistorted", 0, 100, doNothing)

video = cv2.VideoCapture(0)

undistortFisheye = UndistortFisheye()

while True:
    isGrabbed, frame = video.read()
    if not isGrabbed:
        break

    balance = cv2.getTrackbarPos("balance", "Undistorted")/100
    clearImage1 = undistortFisheye.undistort(frame)
    clearImage2 = undistortFisheye.undistort2(frame, balance=balance)

    clearImages = np.hstack((clearImage1, clearImage2))
    cv2.imshow("Undistorted", clearImages)
    # cv2.imshow("Video", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord("s"):
        cv2.imwrite("RawImage2.jpg", frame)

cv2.destroyAllWindows()
