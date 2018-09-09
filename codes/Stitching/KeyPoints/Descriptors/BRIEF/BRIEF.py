from __future__ import print_function
import argparse
import cv2
from imutils import paths
from imutils.video import FPS
from myPackage.KeyPointDetectors import KeyPoints

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="Path to the image")
args = vars(ap.parse_args())


imagePaths = list(paths.list_images(args["dataset"]))
fps = FPS().start()
for (i, imagePath) in enumerate(imagePaths):
    filename = imagePath[imagePath.rfind("/") + 1:]
    image = cv2.imread(imagePath)

    HarrisKeyPoints = KeyPoints(image)
    BRIEF = cv2.BriefDescriptorExtractor_create()
    kp, des = BRIEF.compute(image, HarrisKeyPoints)


    #cv2.imshow("Harris", outputImage)
    #cv2.waitKey()
fps.stop()
print("Elasped time: {:.2f}".format(fps.elapsed()))