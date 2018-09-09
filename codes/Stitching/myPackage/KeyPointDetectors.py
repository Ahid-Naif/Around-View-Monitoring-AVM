import cv2
import numpy as np

class detectKeypoints:
    def __init__(self, image):
        self.image = image
        self.imageCopy = self.image.copy()
        self.gray = cv2.cvtColor(self.imageCopy, cv2.COLOR_BGR2GRAY)

    def detectFAST(self):
        fast = cv2.FastFeatureDetector_create()
        fastKeyPoints = fast.detect(self.gray, None)
        imageFAST = cv2.drawKeypoints(self.imageCopy, fastKeyPoints, self.imageCopy, color=(0, 255, 255))

        return imageFAST

    def detectHarris(self):
        gray = np.float32(self.gray)
        harrisKeyPoints = cv2.cornerHarris(gray, 2, 3, 0.04)  # blockSize -eigen values-, kernel size
        harrisKeyPoints = cv2.dilate(harrisKeyPoints, None)
        self.imageCopy[harrisKeyPoints > 0.01 * harrisKeyPoints.max()] = [0, 255, 255]
        return self.imageCopy

    def detectORB(self, getKeypoints=False):
        ORB = cv2.ORB_create()
        ORBKeyPoints = ORB.detect(self.gray, None)
        self.imageCopy = cv2.drawKeypoints(self.image, ORBKeyPoints, self.imageCopy, color=(0, 255, 255), flags=0)

        if getKeypoints:
            return self.imageCopy, ORBKeyPoints
        else:
            return self.imageCopy

    def detectSIFT(self):
        SIFT = cv2.xfeatures2d.SIFT_create()
        SIFTkeyPoints = SIFT.detect(self.gray, None)
        self.imageCopy = cv2.drawKeypoints(self.gray, SIFTkeyPoints, self.imageCopy)

        return self.imageCopy

    def detectSURF(self):
        SURF = cv2.xfeatures2d.SURF_create()
        SURFKeyPoints = SURF.detect(self.gray, None)
        outputImage = self.imageCopy = cv2.drawKeypoints(self.gray, SURFKeyPoints, self.imageCopy)
        return outputImage
