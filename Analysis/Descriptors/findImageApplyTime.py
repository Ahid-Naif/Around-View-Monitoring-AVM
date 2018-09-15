# the purpose of this code is to calculate the time needed to
# apply the descriptors on different sets of images
from __future__ import print_function
from imutils import paths
from imutils.video import FPS
import cv2
from myPackage.KeyPointDetectors import detectKeypoints
from myPackage.KeyPointsDescriptors import computeKeypoints
import glob

totalTime = 0
for x in range(0,99):
    subTotalTime = 0
    for imagePath in glob.glob("dataset/Images/Random/*"):

        image = cv2.imread(imagePath)
        
        ORB = detectKeypoints(image)
        (outputImage, keypoints) = ORB.detectORB(True)
        fps = FPS().start()
        SURF = computeKeypoints(image, keypoints)
        kps, des = SURF.computeSURF()
        fps.stop()
        subTotalTime = subTotalTime + fps.elapsed()
    totalTime = totalTime + subTotalTime

print("Average elapsed time: ", totalTime/100)