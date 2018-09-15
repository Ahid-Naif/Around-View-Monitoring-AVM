# the purpose of this code is to calculate the time needed to
# apply the detectors on different sets of images
from __future__ import print_function
import argparse
from imutils import paths
from imutils.video import FPS
import cv2
from myPackage.KeyPointDetectors import detectKeypoints

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="Path to the image")
args = vars(ap.parse_args())

totalTime = 0
for x in range(0,99):
    imagePaths = list(paths.list_images(args["dataset"]))
    fps = FPS().start()
    for (i, imagePath) in enumerate(imagePaths):
        filename = imagePath[imagePath.rfind("/") + 1:]
        image = cv2.imread(imagePath)

        keyPoints = detectKeypoints(image)
        outputImage = keyPoints.detectFAST()

        #cv2.imshow("Output", outputImage)
        #cv2.waitKey()
    fps.stop()
    totalTime = totalTime + fps.elapsed()

print("Average elapsed time: ", totalTime/100)