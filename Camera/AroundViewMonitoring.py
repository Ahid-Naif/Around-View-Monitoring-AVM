import cv2
import numpy as np
from Camera.Undistortion import UndistortFisheye
from Camera.PerspectiveTransformation import EagleView

class avm:
    def __init__(self):
        self.__frontCamera = UndistortFisheye("Front_Camera")
        self.__backCamera = UndistortFisheye("Back_Camera")

        self.__frontEagle = EagleView()
        self.__backEagle = EagleView()
        self.__frontEagle.setDimensions((188, 197), (478, 207), (579, 395), (96, 362))
        self.__backEagle.setDimensions((171, 240), (469, 240), (603, 452), (52, 441))
    
    def runAVM(self, frontFrame, backFrame):
        frontView = self.__frontCamera.undistort(frontFrame)
        topDown_Front = self.__frontEagle.transfrom(frontView)
        backView = self.__backCamera.undistort(backFrame)
        topDown_Back = self.__backEagle.transfrom(backView)

        return topDown_Front, topDown_Back