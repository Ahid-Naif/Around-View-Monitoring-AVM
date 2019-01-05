import cv2
import imutils
from imutils.video import FPS
import time
from Camera.Stitcher import stitchTwoImages
from Camera.Undistortion import UndistortFisheye
from Camera.PerspectiveTransformation import EagleView

frontCamera = UndistortFisheye("Front_Camera")
frontEagle = EagleView()
frontEagle.setDimensions((149, 195), (439, 207), (528, 380), (37, 374))

count = 0
totalTime = 0
mergedImage = 0
video = cv2.VideoCapture("dataset/front_camera.avi")
while True:
    count += 1
    isGrabbed, frame = video.read()

    if(not isGrabbed):
        break
    if count % 5 != 0:
        continue
    frontView = frontCamera.undistort(frame)
    topDown_Front = frontEagle.transfrom(frontView)
    # frame = imutils.resize(frame, width=600)
    if count == 5:
        bottom = topDown_Front
    else:
        # time.sleep(1)
        upper = topDown_Front
        cv2.imshow("upper", upper)
        cv2.imshow("bottom", bottom)
        cv2.waitKey()
        # key = cv2.waitKey(1) & 0xFF
        # if key == ord("q"):
        #     break
        stitcher = stitchTwoImages("Bottom2Upper")
        mergedImage = stitcher.stitch(bottom, upper)
        if mergedImage is None:
            continue

        bottom = mergedImage

cv2.imwrite("Result.jpg", mergedImage)