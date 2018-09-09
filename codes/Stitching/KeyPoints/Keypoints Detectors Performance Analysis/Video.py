from __future__ import print_function
import argparse
from imutils.video import FPS
from myPackage.KeyPointDetectors import KeyPoints
import cv2

frameNumber = 0
shortestTime = None
shortestFrame = 1
shortestImage = None
longestTime = None
longestFrame = 1
longestImage = None

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, help="Path to the video")
args = vars(ap.parse_args())

video = cv2.VideoCapture(args["video"])
textFile = open("FAST.txt", "w")

while True:
    (isGrabbed, frame) = video.read()

    if not isGrabbed:
        cv2.imwrite("Longest.jpg", longestImage)
        cv2.imwrite("Shortest.jpg", shortestImage)
        break

    fps = FPS().start()
    keypoints = KeyPoints(frame)
    outputImage = keypoints.getFAST()
    fps.stop()

    elapsedTime = fps.elapsed()
    frameNumber += 1

    textFile.write("{0}, {1}\n".format(frameNumber, elapsedTime))

    if frameNumber == 1:
        shortestTime = elapsedTime
        longestTime = elapsedTime
        shortestImage = outputImage
        longestImage = outputImage
    if elapsedTime < shortestTime:
        shortestTime = elapsedTime
        shortestFrame = frameNumber
        shortestImage = outputImage
    if elapsedTime > longestTime:
        longestTime = elapsedTime
        longestFrame = frameNumber
        longestImage = outputImage

print("#Frames : ", frameNumber)
print("Longest Time: {:.2f}, frame number: {1}", longestTime, longestFrame)
print("Shortest Time: {:.2f}, frame number: {1}", shortestTime, shortestFrame)
cv2.destroyAllWindows()
textFile.close()