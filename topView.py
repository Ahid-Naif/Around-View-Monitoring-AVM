"""
This code is used to obtain the bird's view of
a robot with two cameras installed(front and back cameras)
"""
import cv2
from Camera.Undistortion import UndistortFisheye
from Camera.PerspectiveTransformation import EagleView

frontStream = cv2.VideoCapture(0)
backStream = cv2.VideoCapture(1)

frontCamera = UndistortFisheye("Front_Camera")
backCamera = UndistortFisheye("Back_Camera")

frontEagle = EagleView()
backEagle = EagleView()
frontEagle.setDimensions((149, 195), (439, 207), (528, 380), (37, 374))
backEagle.setDimensions((164, 229), (469, 229), (588, 430), (45, 435))

while True:
    _, frontFrame = frontStream.read()
    _, backFrame = backStream.read()

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