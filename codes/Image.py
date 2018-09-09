# the purpose of this code is to calculate the time needed to
# apply the descriptors on different sets of images
from __future__ import print_function
import argparse
from imutils import paths
from imutils.video import FPS
import cv2
from myPackage.KeyPointDetectors import detectKeypoints
from myPackage.KeyPointsDescriptors import computeKeypoints

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="Path to the image")
args = vars(ap.parse_args())

totalTime = 0
for x in range(0,99):
    imagePaths = list(paths.list_images(args["dataset"]))
    subTotalTime = 0
    for (i, imagePath) in enumerate(imagePaths):
        filename = imagePath[imagePath.rfind("/") + 1:]
        image = cv2.imread(imagePath)

        ORB = detectKeypoints(image)
        (outputImage, keypoints) = ORB.detectORB(True)
        fps = FPS().start()
        SURF = computeKeypoints(image, keypoints)
        kps, des = SURF.computeBRIEF()
        fps.stop()
        subTotalTime = subTotalTime + fps.elapsed()

    totalTime += subTotalTime

averageTotalTime = totalTime/100
averageTotalTime *= 1000  # convert from seconds into milliseconds
print("Average elapsed time: ", averageTotalTime)