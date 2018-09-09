import cv2
import numpy as np
from myPackage.KeyPointDetectors import detectKeypoints
from myPackage.KeyPointsDescriptors import computeKeypoints

class stitchTwoImages:
    def __init__(self, image1, image2):
        self.image1 = image1
        self.image2 = image2

    def stitch(self):
        ORBDet1 = detectKeypoints(self.image1)
        (_, ORBKeypoints1) = ORBDet1.detectORB(True)
        ORBDes1 = computeKeypoints(self.image1, ORBKeypoints1)
        kps1, des1 = ORBDes1.computeBRIEF()

        ORBDet2 = detectKeypoints(self.image2)
        _, ORBKeypoints2 = ORBDet2.detectORB(True)
        ORBDes2 = computeKeypoints(self.image2, ORBKeypoints2)
        kps2, des2 = ORBDes2.computeORB()

        # convert the keypoints from KeyPoint objects to NumPy
        # arrays
        Kps1 = np.float32([kp1.pt for kp1 in kps1])
        Kps2 = np.float32([kp2.pt for kp2 in kps2])

        matcher = cv2.DescriptorMatcher_create("BruteForce")

        matchedKps = matcher.knnMatch(des1, des2, k=2)

        matches = []
        for oneMatch in matchedKps:
            if len(oneMatch) == 2 and oneMatch[0].distance < oneMatch[1].distance * 0.75:
                matches.append((oneMatch[0].trainIdx, oneMatch[0].queryIdx))

        if len(matches) > 4:
            points1 = np.float32([Kps1[i] for (_, i) in matches])
            points2 = np.float32([Kps2[i] for (i, _) in matches])

            (homographyMatrix, status) = cv2.findHomography(points1, points2, cv2.RANSAC, 4)

            newHeight = self.image1.shape[0]
            newWidth = self.image2.shape[1] + self.image2.shape[1]
            # warp the img1 which is on the right
            result = cv2.warpPerspective(self.image1, homographyMatrix, (newWidth, newHeight))

            result[0:self.image2.shape[0], 0:self.image2.shape[1]] = self.image2

            return result