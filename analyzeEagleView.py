"""
This code is used to visualize the bird's view
Meanwhile, it's possible to tune the rectangle corners of which 
the bird's will be obtained
"""
from Camera.PerspectiveTransformation import EagleView
from TrackBar.customizedTrackBar import customizedTrackBar
from Camera.Undistortion import UndistortFisheye
import cv2

# video = cv2.VideoCapture("dataset/front_camera.avi")

camera = UndistortFisheye("Front_Camera")

eagleView = EagleView()

width = 640
height = 480

topLeft_XBar = customizedTrackBar(0, 1, width, 0, "x_topLeft", "Tuning Parameters")
topLeft_YBar = customizedTrackBar(0, 1, height, 0, "y_topLeft", "Tuning Parameters")

topRight_XBar = customizedTrackBar(0, 1, width, width-1, "x_topRight", "Tuning Parameters")
topRight_YBar = customizedTrackBar(0, 1, height, 0, "y_topRight", "Tuning Parameters")

bottomRight_XBar = customizedTrackBar(0, 1, width, width-1, "x_bottomRight", "Tuning Parameters")
bottomRight_YBar = customizedTrackBar(0, 1, height, height-1, "y_bottomRight", "Tuning Parameters")

bottomLeft_XBar = customizedTrackBar(0, 1, width, 0, "x_bottomLeft", "Tuning Parameters")
bottomLeft_YBar = customizedTrackBar(0, 1, height, height-1, "y_bottomLeft", "Tuning Parameters")

while True:
    # isGrabbed, frame = video.read()
    frame = cv2.imread("dataset/Front_View.jpg")

    topLeft = (int(topLeft_XBar.getValue()), int(topLeft_YBar.getValue()))
    topRight = (int(topRight_XBar.getValue()), int(topRight_YBar.getValue()))
    bottomRight = (int(bottomRight_XBar.getValue()), int(bottomRight_YBar.getValue()))
    bottomLeft = (int(bottomLeft_XBar.getValue()), int(bottomLeft_YBar.getValue()))

    cameraView = camera.undistort(frame)
    
    eagleView.setDimensions(topLeft, topRight, bottomRight, bottomLeft)
    topDown = eagleView.transfrom(cameraView)

    cloneFrame = cameraView.copy()
    # visualize corners
    cv2.line(cloneFrame, topLeft, topRight, (0, 0, 255), 1)
    cv2.line(cloneFrame, bottomLeft, bottomRight, (0, 0, 255), 1)
    cv2.line(cloneFrame, topLeft, bottomLeft, (0, 0, 255), 1)
    cv2.line(cloneFrame, bottomRight, topRight, (0, 0, 255), 1)

    cv2.imshow("Bird's Eye View", topDown)
    cv2.imshow("Original Image", cloneFrame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("d"): # print tuned values when "d" button is pressed
        print("width: " + str(cloneFrame.shape[1]))
        print("height: " + str(cloneFrame.shape[0]))

        print("topLeft: " + str(topLeft))
        print("topRight: " + str(topRight))
        print("bottomRight: " + str(bottomRight))
        print("bottomLeft: " + str(bottomLeft))
    elif key == ord("s"):
        cv2.imwrite("Back_View.jpg", frame)

cv2.destroyAllWindows()