import numpy as np
import cv2

frontCamera = cv2.VideoCapture(0)
backCamera = cv2.VideoCapture(1)

fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
frontRecorder = cv2.VideoWriter('front_camera.avi', fourcc, 30.0, (640,480))
backRecorder = cv2.VideoWriter('back_camera.avi', fourcc, 30.0, (640,480))
while True:
    isGrabbed, frontFrame = frontCamera.read()
    isGrabbed2, backFrame = backCamera.read()
    if not isGrabbed and not isGrabbed2:
        break
    
    frontRecorder.write(frontFrame)
    backRecorder.write(backFrame)

    cv2.imshow("Front Camera", frontFrame)
    cv2.imshow("Back Recorder", backFrame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()