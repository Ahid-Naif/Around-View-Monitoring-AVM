import cv2

class computeKeypoints:
    def __init__(self, image, keypoints):
        self.image = image
        self.keypoints = keypoints
        self.imageCopy = self.image.copy()
        self.gray = cv2.cvtColor(self.imageCopy, cv2.COLOR_BGR2GRAY)

    def computeORB(self):
        ORB = cv2.ORB_create()
        kps, des = ORB.compute(self.image, self.keypoints)

        return kps, des

    def computeBRIEF(self):
        BRIEF = cv2.xfeatures2d.BriefDescriptorExtractor_create()
        kps, des = BRIEF.compute(self.image, self.keypoints)

        return kps, des

    def computeSIFT(self):
        SIFT = cv2.xfeatures2d.SIFT_create()
        kps, des = SIFT.compute(self.gray, None)

        return kps, des

    def computeSURF(self):
        SURF = cv2.xfeatures2d.SURF_create()
        kps, des = SURF.compute(self.image, None)

        return kps, des



