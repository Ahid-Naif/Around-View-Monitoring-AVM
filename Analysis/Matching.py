# import the necessary packages
from __future__ import print_function
import numpy as np
import argparse
import cv2
from myPackage.KeyPointDetectors import detectKeypoints
from myPackage.KeyPointsDescriptors import computeKeypoints

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--first", required=True, help="Path to first image")
ap.add_argument("-s", "--second", required=True, help="Path to second image")
args = vars(ap.parse_args())

image1 = cv2.imread(args["first"])
image2 = cv2.imread(args["second"])

# Initiate ORB detector
ORB = cv2.ORB_create()

det1 = detectKeypoints(image1)
(_, kps1) = det1.detectORB(True)
des1 = computeKeypoints(image1, kps1)
kps1, des1 = des1.computeORB()

det2 = detectKeypoints(image2)
(_, kps2) = det2.detectORB(True)
des2 = computeKeypoints(image2, kps2)
kps2, des2 = des2.computeORB()

# create BFMatcher object
matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

matches = matcher.match(des1, des2)

# Sort them in the order of their distance.
matches = sorted(matches, key=lambda x: x.distance)
# initialize the output visualization image
image3 = cv2.drawMatches(image1,kps1,image2,kps2,matches[0:30],outImg=image2,flags=2)

print("# of matched keypoints: {}".format(len(matches)))
cv2.imshow("Output", image3)
cv2.imwrite("ORB.jpg", image3)
cv2.waitKey()