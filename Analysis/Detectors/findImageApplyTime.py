# the purpose of this code is to calculate the time needed to
# apply the detectors on different sets of images
from __future__ import print_function
from imutils import paths
from imutils.video import FPS
import cv2
from myPackage.KeyPointDetectors import detectKeypoints
import glob

totalTime = 0
for x in range(0,99):
    subTotalTime = 0
    for imagePath in glob.glob("dataset/Images/Random/*"):

        image = cv2.imread(imagePath)

        fps = FPS().start()
        keyPoints = detectKeypoints(image)
        outputImage = keyPoints.detectFAST()
        fps.stop()
        subTotalTime = subTotalTime + fps.elapsed()

    totalTime = totalTime + subTotalTime

print("Average elapsed time: ", totalTime/100)