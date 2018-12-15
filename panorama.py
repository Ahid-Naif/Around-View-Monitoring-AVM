import cv2
import imutils
from imutils.video import FPS

from Camera.Stitcher import stitchTwoImages

count = 0
totalTime = 0
mergedImage = 0
video = cv2.VideoCapture("dataset/IMG_5006.MOV")
while True:
    isGrabbed, frame = video.read()

    if(not isGrabbed):
        break

    resizedFrame = imutils.resize(frame, width=800)
    if count == 0:
        image1 = resizedFrame
    else:
        image2 = resizedFrame
        fps = FPS().start()
        stitcher = stitchTwoImages(image1, image2, "Right2Left")
        mergedImage = stitcher.stitch()
        fps.stop()
        totalTime = totalTime + fps.elapsed()

        image1 = mergedImage

    count += 1

cv2.imwrite("Result.jpg", mergedImage)
print("Elapsed time: ", totalTime)