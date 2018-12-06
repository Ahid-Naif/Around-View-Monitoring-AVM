import cv2
import numpy as np
import imutils
from Camera.Undistortion import UndistortFisheye
from Camera.PerspectiveTransformation import EagleView

class avm:
    def __init__(self):
        self.__frontCamera = UndistortFisheye("Front_Camera")
        self.__backCamera = UndistortFisheye("Back_Camera")

        self.__frontEagle = EagleView()
        self.__backEagle = EagleView()
        self.__frontEagle.setDimensions((149, 195), (439, 207), (528, 380), (37, 374))
        self.__backEagle.setDimensions((164, 229), (469, 229), (588, 430), (45, 435))
    
    def runAVM(self, frontFrame, backFrame):
        frontView = self.__frontCamera.undistort(frontFrame)
        topDown_Front = self.__frontEagle.transfrom(frontView)
        backView = self.__backCamera.undistort(backFrame)
        topDown_Back = self.__backEagle.transfrom(backView)

        topDown_Front , topDown_Back = self.__reScale(topDown_Front, topDown_Back)
        middleView = self.__getMiddleView(topDown_Front)
        birdView = np.vstack((topDown_Front, middleView, topDown_Back))
        return birdView
    
    def __reScale(self, topDown_Front, topDown_Back):
        width_FrontView = topDown_Front.shape[1]
        width_BackView = topDown_Back.shape[1]
        height_FrontView = topDown_Front.shape[0]
        height_BackView = topDown_Back.shape[0]

        if width_FrontView > width_BackView:
            newWidth = width_BackView
            ratio = width_BackView/width_FrontView
            newHeight = int(ratio * height_FrontView)
            topDown_Front = cv2.resize(topDown_Front, (newWidth, newHeight))
        else:
            newWidth = width_FrontView
            ratio = width_FrontView/width_BackView
            newHeight = int(ratio * height_BackView)
            topDown_Back = cv2.resize(topDown_Back, (newWidth, newHeight))
        
        return topDown_Front, topDown_Back
    
    def __getMiddleView(self, topDown_Front):
        # the length of the image represents the distance in front or back of the car
        height_FrontView = topDown_Front.shape[0]
        
        realHeight_FrontView = 13 # unit is cm
        realHeight_MiddleView = 29.5 # unit is cm
        height_MiddleView = int(realHeight_MiddleView/realHeight_FrontView * height_FrontView)
        width_MiddleView = int(topDown_Front.shape[1])  
        middleView = np.zeros((height_MiddleView, width_MiddleView, 3), np.uint8)
        return middleView