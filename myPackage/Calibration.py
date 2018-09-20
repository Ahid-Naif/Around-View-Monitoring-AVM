import cv2
import numpy as np

def calibrate(img):

    H11 = 2350.6
    H12 = 0
    H13 = 314.3
    H21 = 0
    H22 = 237.5
    H23 = 233.2
    H31 = 0.0
    H32 = 0.0
    H33 = 1.0

    K = np.array([[H11, H12, H13],
                  [H21, H22, H23],
                  [H31, H32, H33]])

    D = np.array([[0.01535], [-0.1092], [0.1003], [-0.03689]]) # ignore distortion vector for the moment

    Knew = np.identity(3, dtype=float)

    undistortedImage = cv2.fisheye.undistortImage(img, K, D=D, Knew=Knew) # how does work?

    return undistortedImage




    