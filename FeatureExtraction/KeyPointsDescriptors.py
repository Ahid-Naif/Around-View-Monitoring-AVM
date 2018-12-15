import cv2

class computeKeypoints:
    def __init__(self):
        pass
    
    def computeORB(self, image, keypoints):
        ORB = cv2.ORB_create()
        kps, des = ORB.compute(image, keypoints)

        return kps, des

    def computeBRIEF(self, image, keypoints):
        BRIEF = cv2.xfeatures2d.BriefDescriptorExtractor_create()
        kps, des = BRIEF.compute(image, keypoints)

        return kps, des

    def computeSIFT(self, image, keypoints):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        SIFT = cv2.xfeatures2d.SIFT_create()
        kps, des = SIFT.compute(gray, keypoints)

        return kps, des

    def computeSURF(self, image, keypoints):
        SURF = cv2.xfeatures2d.SURF_create()
        kps, des = SURF.compute(image, keypoints)

        return kps, des