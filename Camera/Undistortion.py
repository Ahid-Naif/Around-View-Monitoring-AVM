import cv2
import numpy as np
import re
from TrackBar.customizedTrackBar import customizedTrackBar
class UndistortFisheye:
    def __init__(self, cameraName, tune=False):
        self.tune = tune
        self.width  = 0
        self.height = 0
        self.fx = 0.0
        self.fy = 0.0
        self.cx = 0.0
        self.cy = 0.0
        self.dOne  = 0.0
        self.dTwo  = 0.0
        self.dThree = 0.0
        self.dFour  = 0.0

        regexVariable = r"(\w*)"
        regexValue = r"[-+]?\d*\.\d+|\d+"
        file = open("Parameters/K_D_Values_" + cameraName + ".txt", "r")
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

        if self.tune:
            self.tuneMin = -0.5
            self.tuneMax = 0.5
            self.tuneStep = 0.0001
            self.d1TrackBar = customizedTrackBar(self.tuneMin, self.tuneStep, self.tuneMax, self.dOne, "d1", "Tuning")
            self.d2TrackBar = customizedTrackBar(self.tuneMin, self.tuneStep, self.tuneMax, self.dTwo, "d2", "Tuning")
            self.d3TrackBar = customizedTrackBar(self.tuneMin, self.tuneStep, self.tuneMax, self.dThree, "d3", "Tuning")
            self.d4TrackBar = customizedTrackBar(self.tuneMin, self.tuneStep, self.tuneMax, self.dFour, "d4", "Tuning")

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

    def tuneDistortionVictor(self):
        d1 = self.d1TrackBar.getValue()
        d2 = self.d2TrackBar.getValue()
        d3 = self.d3TrackBar.getValue()
        d4 = self.d4TrackBar.getValue()
        self.D = np.array([[d1], [d2], [d3], [d4]])

    def undistort(self, image):
        if self.tune:
            self.tuneDistortionVictor()
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.K, self.D, np.eye(3), self.K, self.DIM, cv2.CV_16SC2)
        undistortedImage = cv2.remap(image, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        return undistortedImage

    def undistort2(self, image, balance=0.5, dim2=None):
        if self.tune:
            self.tuneDistortionVictor()
        # dim1 = image.shape[:2][::-1]
        # assert dim1[0]/dim1[1] == self.DIM[0]/self.DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"

        # if not dim2:
        #     dim2 = dim1
        
        # Kscaled = self.K * dim1[0]/self.DIM[0] # The values of K is to scale with image dimension
        # Kscaled[2][2] = 1 # the value in 2nd row & 2nd column of K matrix is always 1

        # Knew = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(Kscaled, self.D, dim2, np.eye(3), balance=balance)
        Knew = self.K.copy()
        Knew[(0, 1), (0, 1)] = 0.4 * Knew[(0, 1), (0, 1)]
        undistortedImage = cv2.fisheye.undistortImage(image, self.K, D=self.D, Knew=Knew) # how does work?

        return undistortedImage
    
    def reset(self):
        if self.tune:
            self.d1TrackBar.setDefaultPosition()
            self.d2TrackBar.setDefaultPosition()
            self.d3TrackBar.setDefaultPosition()
            self.d4TrackBar.setDefaultPosition()