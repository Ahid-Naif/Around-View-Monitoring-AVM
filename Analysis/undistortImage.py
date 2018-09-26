import cv2
import numpy as np
from myPackage.UndistortFisheye import UndistortFisheye
import glob

def doNothing(_):
    pass
def warp(image, W1, W2, H1, H2):
    (h, w) = image.shape[:2]

    src = np.array([(int(w / 2) - W1, int(h / 2) - H1), (int(w/ 2) + W2, int(h / 2) - H2), (w, h), (0, h)], dtype="float32")
    dst = np.array([(0, 0), (w, 0), (int(w / 2 + 200), h), (int(w / 2 - 200), h)], dtype="float32")

    M = cv2.getPerspectiveTransform(src, dst)
    eagleEye = cv2.warpPerspective(image, M, (w, h))

    return eagleEye

cv2.namedWindow("TrackBars")
cv2.createTrackbar("balance", "TrackBars", 0, 100, doNothing)
cv2.createTrackbar("W1", "TrackBars", 0, 300, doNothing)
cv2.createTrackbar("W2", "TrackBars", 0, 300, doNothing)
cv2.createTrackbar("H1", "TrackBars", 0, 300, doNothing)
cv2.createTrackbar("H2", "TrackBars", 0, 300, doNothing)

cv2.setTrackbarPos("W1", "TrackBars", 221)
cv2.setTrackbarPos("W2", "TrackBars", 184)
cv2.setTrackbarPos("H1", "TrackBars", 130)
cv2.setTrackbarPos("H2", "TrackBars", 126)

undistortFisheye = UndistortFisheye()

while True:
    image = cv2.imread("RawImage.jpg")

    balance = cv2.getTrackbarPos("balance", "TrackBars")/100
    W1 = cv2.getTrackbarPos("W1", "TrackBars")
    W2 = cv2.getTrackbarPos("W2", "TrackBars")
    H1 = cv2.getTrackbarPos("H1", "TrackBars")
    H2 = cv2.getTrackbarPos("H2", "TrackBars")

    clearImage1 = undistortFisheye.undistort(image)
    clearImage2 = undistortFisheye.undistort2(image, balance=balance)

    topView1 = warp(clearImage1, W1, W2, H1, H2)
    topView2 = warp(clearImage2, W1, W2, H1, H2)

    clearImages = np.hstack((clearImage1, clearImage2))
    topViews = np.hstack((topView1, topView2))
    cv2.imshow("Undistorted", clearImages)
    cv2.imshow("TopView", topViews)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
