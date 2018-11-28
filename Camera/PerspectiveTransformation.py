from scipy.spatial import distance as dist
import numpy as np 
import cv2

"""
- EagleView finds the top-down view of an image
- First, we cut new rectangle shaped dimensions of the original image
- Second, we find the distination dimensions of our recatangle in the top-down view coordintaes
- Third, we find M (Perspective Transform Matrix)
- Finally, we find the top-down view (bird's eye view)
"""
class EagleView:
    def __init__(self):
        self.__topLeft = []
        self.__topRight = []
        self.__bottomRight = []
        self.__bottomLeft = []
        self.__newDimensions = []

        self.__newWidth = None
        self.__newHeight = None
        self.__distanationDimensions = []
        self.__M = [] # Perspective Transform Matrix
    
    def setDimensions(self, topLeft, topRight, bottomRight, bottomLeft):
        self.__topLeft = np.array(topLeft).reshape(1, -1)
        self.__topRight = np.array(topRight).reshape(1, -1)
        self.__bottomRight = np.array(bottomRight).reshape(1, -1)
        self.__bottomLeft = np.array(bottomLeft).reshape(1, -1)
        self.__newDimensions = np.array([self.__topLeft, self.__topRight, self.__bottomRight, self.__bottomLeft], dtype="float32")

    def transfrom(self, image):
        self.__computeNewDimensions()
        self.__computeDistinationDimensions()
        self.__computePerspectiveTransformMatrix()

        eagleView = cv2.warpPerspective(image, self.__M, (self.__newWidth, self.__newHeight))
        return eagleView

    def __computeNewDimensions(self):
        # compute width of new image
        # width of new image is the longest of the distances between topLeft & topRight
        # or between bottomLeft & bottomRight corners
        topWidth = dist.cdist(self.__topLeft, self.__topRight, 'euclidean')
        bottomWidth = dist.cdist(self.__bottomLeft, self.__bottomRight, 'euclidean')
        self.__newWidth = max(int(topWidth), int(bottomWidth))

        # compute height of new image
        # height of new image is the longest of the distances between topLeft & bottomLeft
        # or between topRight or bottomRight corners
        leftHeight = dist.cdist(self.__topLeft, self.__bottomLeft, 'euclidean')
        rightHeight = dist.cdist(self.__topRight, self.__bottomRight, 'euclidean')
        self.__newHeight = max(int(leftHeight), int(rightHeight))        

    def __computeDistinationDimensions(self):
        topLeft = [0, 0]
        topRight = [self.__newWidth - 1, 0]
        bottmRight = [self.__newWidth - 1, self.__newHeight - 1]
        bottomLeft = [0, self.__newHeight - 1]
        self.__distanationDimensions = np.array([topLeft, topRight, bottmRight, bottomLeft], dtype="float32")

    def __computePerspectiveTransformMatrix(self):
        self.__M = cv2.getPerspectiveTransform(self.__newDimensions, self.__distanationDimensions)