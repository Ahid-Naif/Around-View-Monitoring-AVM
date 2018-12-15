import cv2
import numpy as np
from FeatureExtraction.KeyPointDetectors import detectKeypoints
from FeatureExtraction.KeyPointsDescriptors import computeKeypoints

class stitchTwoImages:
    def __init__(self, orientation):
        self.orientation = orientation

        self.kpsDetector = detectKeypoints()
        self.kpsDescriptor = computeKeypoints()

    def stitch(self, image1, image2):
        kps1 = self.kpsDetector.detectORB(image1)
        kps1, des1 = self.kpsDescriptor.computeORB(image1, kps1)

        kps2 = self.kpsDetector.detectORB(image2)
        kps2, des2 = self.kpsDescriptor.computeORB(image2, kps2)

        # convert the keypoints from KeyPoint objects to NumPy
        # arrays
        Kps1 = np.float32([kp1.pt for kp1 in kps1])
        Kps2 = np.float32([kp2.pt for kp2 in kps2])

        _, homographyMatrix, _ = self.__matchKeypoints(Kps1, Kps2, des1, des2)
        width_1 = image1.shape[1]
        height_1 = image1.shape[0]
        width_2 = image2.shape[1]
        height_2 = image2.shape[0]
        newHeight, newWidth = self.__getNewDimensions(homographyMatrix, width_1, height_1, width_2, height_2)
        
        # warp the img1 which is on the right/down
        result = cv2.warpPerspective(image1, homographyMatrix, (newWidth, newHeight))

        result[0:height_2, 0:width_2] = image2
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

    def __getNewDimensions(self, M, width_1, height_1, width_2, height_2):
        x = width_1
        y = height_1
        newX = (x * M[0][0] + y * M[0][1] + M[0][2]) / (x * M[2][0] + y * M[2][1] + M[2][2])
        newY = (x * M[1][0] + y * M[1][1] + M[1][2]) / (x * M[2][0] + y * M[2][1] + M[2][2])

        if self.orientation == "Right2Left":
            newHeight = height_1
            newWidth = width_1 + width_2
            newWidth -= (newWidth - int(newX))
        elif self.orientation == "Bottom2Upper":
            newHeight = height_1 + height_2
            newHeight -= (newHeight - int(newY))
            newWidth = width_1
        
        return newHeight , newWidth 