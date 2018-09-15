import cv2
import numpy as np
from myPackage.KeyPointDetectors import detectKeypoints

img1 = cv2.imread("dataset/Panorama_Images/bryce_right_02.png") # queryImage -- right image
img2 = cv2.imread("dataset/Panorama_Images/bryce_left_02.png") # trainImage -- left image
matcher = cv2.DescriptorMatcher_create("BruteForce")

#SURF1 = KeyPoints(img1)
#kps1 = SURF1.getSURF(drawKeyPoints=False)
#SURF2 = KeyPoints(img2)
#kps2 = SURF2.getSURF(drawKeyPoints=False)

SIFT1 = cv2.xfeatures2d.SIFT_create()
(kps1, des1) = SIFT1.detectAndCompute(img1, None)
kps1 = np.float32([kp.pt for kp in kps1])
SIFT2 = cv2.xfeatures2d.SIFT_create()
(kps2, des2) = SIFT2.detectAndCompute(img2, None)
kps2 = np.float32([kp.pt for kp in kps2])

matchedKps = matcher.knnMatch(des1, des2, 2)
matches = []

for oneMatch in matchedKps:
    if len(oneMatch) == 2 and oneMatch[0].distance < oneMatch[1].distance*0.75:
        matches.append((oneMatch[0].trainIdx, oneMatch[0].queryIdx))

if len(matches) > 4:
    points1 = np.float32([kps1[i] for (_, i) in matches])
    points2 = np.float32([kps2[i] for (i, _) in matches])

    (homographyMatrix, status) = cv2.findHomography(points1, points2, cv2.RANSAC, 4)

    newHeight = img1.shape[0]
    newWidth = img1.shape[1] + img2.shape[1]
    # warp the img1 which is on the right
    result = cv2.warpPerspective(img1, homographyMatrix, (newWidth, newHeight))

    result[0:img2.shape[0], 0:img2.shape[1]] = img2

cv2.imshow("Result", result)
cv2.imwrite("result.png", result)
cv2.waitKey()

#print("# of matched keypoints: {}".format(len(matches)))
#print("# of keypoints from first image: {}".format(len(kps1)))
#print("# of keypoints from second image: {}".format(len(kps2)))