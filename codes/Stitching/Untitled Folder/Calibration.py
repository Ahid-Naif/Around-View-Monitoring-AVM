import numpy as np
import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

def doNothing(_):
    pass

min = 0
max = 1700
maxDistortion = 100

cv2.namedWindow("clearImg", cv2.WINDOW_NORMAL)
#cv2.createTrackbar("H11", "clearImg", min, max, doNothing)
#cv2.createTrackbar("H13", "clearImg", min, max, doNothing)
#cv2.createTrackbar("H22", "clearImg", min, max, doNothing)
#cv2.createTrackbar("H23", "clearImg", min, max, doNothing)

#cv2.setTrackbarPos("H11", "clearImg", 499)
#cv2.setTrackbarPos("H13", "clearImg", 602)
#cv2.setTrackbarPos("H22", "clearImg", 1246)
#cv2.setTrackbarPos("H23", "clearImg", 243)

cv2.createTrackbar("d1", "clearImg", min, maxDistortion, doNothing)
cv2.createTrackbar("d2", "clearImg", min, maxDistortion, doNothing)
cv2.createTrackbar("d3", "clearImg", min, maxDistortion, doNothing)
cv2.createTrackbar("d4", "clearImg", min, maxDistortion, doNothing)

cv2.setTrackbarPos("d1", "clearImg", 0)
cv2.setTrackbarPos("d2", "clearImg", 0)
cv2.setTrackbarPos("d3", "clearImg", 0)
cv2.setTrackbarPos("d4", "clearImg", 0)

def rectify(image):
    #H11 = cv2.getTrackbarPos("H11", "clearImg")
    H11 = 499
    H13 = 602
    H22 = 1246
    H23 = 243

    H12 = 0
    #H13 = cv2.getTrackbarPos("H13", "clearImg")
    H21 = 0
    #H22 = cv2.getTrackbarPos("H22", "clearImg")
    #H23 = cv2.getTrackbarPos("H23", "clearImg")
    H31 = 0
    H32 = 0
    H33 = 1
    H11 = float(H11)
    H12 = float(H12)
    H13 = float(H13)
    H21 = float(H21)
    H22 = float(H22)
    H23 = float(H23)
    H31 = float(H31)
    H32 = float(H32)
    H33 = float(H33)

    K = np.array([[H11, H12, H13],
                  [H21, H22, H23],
                  [H31, H32, H33]])

    d1 = cv2.getTrackbarPos("d1", "clearImg")
    d2 = cv2.getTrackbarPos("d2", "clearImg")
    d3 = cv2.getTrackbarPos("d3", "clearImg")
    d4 = cv2.getTrackbarPos("d4", "clearImg")
    d1 = float(d1)
    d2 = float(d2)
    d3 = float(d3)
    d4 = float(d4)

    D = np.array([d1/100, d2/100, d3/100, d4/100])

    Knew = K.copy()
    Knew[(0, 1), (0, 1)] = 0.4 * Knew[(0, 1), (0, 1)]

    return cv2.fisheye.undistortImage(image, K, D=D, Knew=Knew)

while True:
    image = cv2.imread(args["image"])
    undistortedImage = rectify(image)

    cv2.imshow("clearImg", undistortedImage)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()