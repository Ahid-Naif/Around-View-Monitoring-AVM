import cv2
import numpy as np
import re


class UndistortFisheye:
    def __init__(self):
        self.width  = 0
        self.height = 0
        self.fx = 0.0
        self.fy = 0.0
        self.cx = 0.0
        self.cy = 0.0
        self.dOne  = 0.0
        self.dTwo  = 0.0
        self.Three = 0.0
        self.Four  = 0.0

        regexVariable = r"(\w*)"
        regexValue = r"[-+]?\d*\.\d+|\d+"
        file = open("K_D_Values.txt", "r")
        lines = file.readlines()
        for line in lines:
            variable = re.findall(regexVariable, line)
            value = re.findall(regexValue, line)
            self.setMember(variable[0], value[0])

        self.DIM = (self.width, self.height)
        self.K = np.array([[self.fx,0.0,self.cx],
                          [0.0,self.fy,self.fy],
                          [0.0,0.0,1.0]])
        self.D = np.array([[self.dOne], [self.dTwo], [self.dThree], [self.dFour]])

    def setMember(self, variable, value):
        if variable == "width":
            self.width = int(value)
        elif variable == "height":
            self.height = int(value)
        elif variable == "fx":
            self.fx = float(value)
        elif variable == "fy":
            self.fy = float(value)
        elif variable == "cx":
            self.cx = float(value)
        elif variable == "cy":
            self.cy = float(value)
        elif variable == "dOne":
            self.dOne = float(value)
        elif variable == "dTwo":
            self.dTwo = float(value)
        elif variable == "dThree":
            self.dThree = float(value)
        elif variable == "dFour":
            self.dFour = float(value)

    def undistort(self, image):
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.K, self.D, np.eye(3), self.K, self.DIM, cv2.CV_16SC2)
        undistortedImage = cv2.remap(image, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        return undistortedImage

    def calibrate(self, img):

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