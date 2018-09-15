from __future__ import print_function
import argparse
from imutils import paths
from imutils.video import FPS
import cv2
from myPackage.KeyPointDetectors import detectKeypoints

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="Path to the image")
args = vars(ap.parse_args())


imagePaths = list(paths.list_images(args["dataset"]))
fps = FPS().start()
for (i, imagePath) in enumerate(imagePaths):
    filename = imagePath[imagePath.rfind("/") + 1:]
    image = cv2.imread(imagePath)

    FASTKeyPoints = detectKeypoints(image)
    outputImage = FASTKeyPoints.detectFAST()

    cv2.imshow("FAST", outputImage)
    cv2.waitKey()
fps.stop()
print("Elasped time: {:.2f}".format(fps.elapsed()))