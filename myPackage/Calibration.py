import cv2
import numpy as np

def calibrate(img):

    H11 = 0
    H12 = 0
    H13 = 0
    H21 = 0
    H22 = 0
    H23 = 0
    H31 = 0
    H32 = 0
    H33 = 0

    K = np.array([[H11], [H12], [H13],
                  [H21], [H22], [H23],
                  [H31], [H32], [H33]])

    D = np.array(0.0, 0.0, 0.0, 0.0) # ignore distortion vector for the moment

    Knew = K.copy()
    Knew[(0,1), (0,1)] *= 0.4 # what is this line for?

    undistortedImage = cv2.fisheye.undistortImage(img, K, D=D, Knew=Knew) # how does work?

    return undistortedImage




    