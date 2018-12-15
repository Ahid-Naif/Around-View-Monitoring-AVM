import cv2
import numpy as np

class detectKeypoints:
    def __init__(self):
       pass

    def detectFAST(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fast = cv2.FastFeatureDetector_create()
        fastKeyPoints = fast.detect(gray, None)
        # imageFAST = cv2.drawKeypoints(self.imageCopy, fastKeyPoints, self.imageCopy, color=(0, 255, 255))

        return fastKeyPoints

    def detectHarris(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = np.float32(gray)
        harrisKeyPoints = cv2.cornerHarris(gray, 2, 3, 0.04)  # blockSize -eigen values-, kernel size
        harrisKeyPoints = cv2.dilate(harrisKeyPoints, None)
        # self.imageCopy[harrisKeyPoints > 0.01 * harrisKeyPoints.max()] = [0, 255, 255]
        return harrisKeyPoints

    def detectORB(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ORB = cv2.ORB_create()
        ORBKeyPoints = ORB.detect(gray, None)
        # self.imageCopy = cv2.drawKeypoints(self.image, ORBKeyPoints, self.imageCopy, color=(0, 255, 255), flags=0)

        # if getKeypoints:
        #     return self.imageCopy, ORBKeyPoints
        # else:
        return ORBKeyPoints

    def detectSIFT(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        SIFT = cv2.xfeatures2d.SIFT_create()
        SIFTkeyPoints = SIFT.detect(gray, None)
        # self.imageCopy = cv2.drawKeypoints(self.gray, SIFTkeyPoints, self.imageCopy)

        return SIFTkeyPoints

    def detectSURF(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        SURF = cv2.xfeatures2d.SURF_create()
        SURFKeyPoints = SURF.detect(gray, None)
        # outputImage = self.imageCopy = cv2.drawKeypoints(self.gray, SURFKeyPoints, self.imageCopy)
        return SURFKeyPoints