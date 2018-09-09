import argparse
import cv2
import imutils

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
copy = image.copy()
output = imutils.resize(copy, width = 400)

cv2.imwrite("7.jpeg", output)

