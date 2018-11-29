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
        self.__frontEagle.setDimensions((210, 108), (425, 115), (587, 345), (44, 335))
        self.__backEagle.setDimensions((210, 108), (425, 115), (587, 345), (44, 335))
    
    def runAVM(self, frontFrame, backFrame):
        frontView = self.__frontCamera.undistort(frontFrame)
        topDown_Front = self.__frontEagle.transfrom(frontView)
        backView = self.__backCamera.undistort(backFrame)
        topDown_Back = self.__backEagle.transfrom(backView)

        birdView = np.vstack((topDown_Front, topDown_Back))

        return birdView