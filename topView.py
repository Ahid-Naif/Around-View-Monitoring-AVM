"""
This code is used to obtain the bird's view of
a robot with two cameras installed(front and back cameras)
"""
import cv2
from Camera.Undistortion import UndistortFisheye
from Camera.PerspectiveTransformation import EagleView

# frontStream = cv2.VideoCapture("dataset/front_camera.avi")
# backStream = cv2.VideoCapture("dataset/back_camera.avi")

frontCamera = UndistortFisheye("Front_Camera")
backCamera = UndistortFisheye("Back_Camera")

frontEagle = EagleView()
backEagle = EagleView()
frontEagle.setDimensions((186, 195), (484, 207), (588, 402), (97, 363))
backEagle.setDimensions((171, 240), (469, 240), (603, 452), (52, 441))

while True:
    # _, frontFrame = frontStream.read()
    # _, backFrame = backStream.read()
    frontFrame = cv2.imread("dataset/Front_View.jpg")
    backFrame = cv2.imread("dataset/Rear_View.jpg")
    
    frontView = frontCamera.undistort(frontFrame)
    topDown_Front = frontEagle.transfrom(frontView)
    backView = backCamera.undistort(backFrame)
    topDown_Back = backEagle.transfrom(backView)

    cv2.imshow("Front Bird's Eye View", topDown_Front)
    cv2.imshow("Back Bird's Eye View", topDown_Back)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()