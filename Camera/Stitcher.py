import cv2
import numpy as np
from FeatureExtraction.KeyPointDetectors import detectKeypoints
from FeatureExtraction.KeyPointsDescriptors import computeKeypoints

class stitchTwoImages:
    def __init__(self, image1, image2, orientation):
        self.image1 = image1
        self.image2 = image2
        self.orientation = orientation

        self.kpsDetector = detectKeypoints()
        self.kpsDescriptor = computeKeypoints()

    def stitch(self):
        kps1 = self.kpsDetector.detectORB(self.image1)
        kps1, des1 = self.kpsDescriptor.computeORB(self.image1, kps1)

        kps2 = self.kpsDetector.detectORB(self.image2)
        kps2, des2 = self.kpsDescriptor.computeORB(self.image2, kps2)

        # convert the keypoints from KeyPoint objects to NumPy
        # arrays
        Kps1 = np.float32([kp1.pt for kp1 in kps1])
        Kps2 = np.float32([kp2.pt for kp2 in kps2])

        _, homographyMatrix, _ = self.__matchKeypoints(Kps1, Kps2, des1, des2)

        newHeight, newWidth = self.__getNewDimensions(homographyMatrix)
        
        
        # warp the img1 which is on the right/down
        result = cv2.warpPerspective(self.image1, homographyMatrix, (newWidth, newHeight))

        result[0:self.image2.shape[0], 0:self.image2.shape[1]] = self.image2
        return result
    
    def __matchKeypoints(self, kps1, kps2, des1, des2):
        matcher = cv2.DescriptorMatcher_create("BruteForce")

        matchedKps = matcher.knnMatch(des1, des2, k=2)

        matches = []
        for oneMatch in matchedKps:
            if len(oneMatch) == 2 and oneMatch[0].distance < oneMatch[1].distance * 0.75:
                matches.append((oneMatch[0].trainIdx, oneMatch[0].queryIdx))

        if len(matches) > 4:
            points1 = np.float32([kps1[i] for (_, i) in matches])
            points2 = np.float32([kps2[i] for (i, _) in matches])

            (homographyMatrix, status) = cv2.findHomography(points1, points2, cv2.RANSAC, 4)
            return matches, homographyMatrix, status
        else:
            return None

    def __getNewDimensions(self, M):
        x = self.image1.shape[1]
        y = self.image1.shape[0]
        newX = (x * M[0][0] + y * M[0][1] + M[0][2]) / (x * M[2][0] + y * M[2][1] + M[2][2])
        newY = (x * M[1][0] + y * M[1][1] + M[1][2]) / (x * M[2][0] + y * M[2][1] + M[2][2])

        if self.orientation == "Right2Left":
            newHeight = self.image1.shape[0]
            newWidth = self.image2.shape[1] + self.image2.shape[1]
            newWidth -= (newWidth - int(newX))
        elif self.orientation == "Bottom2Upper":
            newHeight = self.image1.shape[0] + self.image2.shape[0]
            newHeight -= (newHeight - int(newY))
            newWidth = self.image1.shape[1]
        
        return newHeight , newWidth 