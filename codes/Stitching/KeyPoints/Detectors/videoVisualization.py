# the purpose of this code is to visualize the detected keypoints
# on a running video
import argparse
import cv2
from myPackage.KeyPointDetectors import KeyPoints
import time

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, help="Path to the video")
args = vars(ap.parse_args())

video = cv2.VideoCapture(args["video"])

while True:
    (isGrabbed, frame) = video.read()
    time.sleep(0.0331)

    if (not isGrabbed) and args.get("video"):
        break

    keypoints = KeyPoints(frame)
    outputImage = keypoints.getFAST()

    cv2.imshow("Video", outputImage)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()