import cv2
import numpy as np

def calibrate(img):

    H11 = 1
    H12 = 2
    H13 = 3
    H21 = 4
    H22 = 5
    H23 = 6
    H31 = 7
    H32 = 8
    H33 = 9

    K = np.array([[H11, H12, H13],
                  [H21, H22, H23],
                  [H31, H32, H33]])

    D = np.array([0.0, 0.0, 0.0, 0.0]) # ignore distortion vector for the moment

    Knew = 0.4 * np.identity(3, dtype=float)

    undistortedImage = cv2.fisheye.undistortImage(img, K, D=D, Knew=Knew) # how does work?

    return undistortedImage




    