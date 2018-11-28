"""
This code uses the output parameters of the camera calibration
to get a clear image(undistorted) by remapping it
"""
import cv2
from Camera.Undistortion import UndistortFisheye

frontStream = cv2.VideoCapture(0)
backStream = cv2.VideoCapture(0)

frontCamera = UndistortFisheye("Front_Camera")
backCamera = UndistortFisheye("Back_Camera")

while True:
    _, frontFrame = frontStream.read()
    _, backFrame = backStream.read()

    frontView = frontCamera.undistort(frontFrame)
    backView = backCamera.undistort(backFrame)

    cv2.imshow("Undistorted Front", frontView)
    cv2.imshow("Undistorted Back", backView)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord("s"):
        cv2.imwrite("Capture.jpg", frontView)
    
    if key == ord("r"):
        frontCamera.reset() 
        backCamera.reset()   

cv2.destroyAllWindows()