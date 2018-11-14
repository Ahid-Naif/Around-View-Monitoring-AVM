from PerspectiveTransformation.EagleView import EagleView
from myPackage.customizedTrackBar import customizedTrackBar
import numpy as np
import cv2

eagleView = EagleView()
image = cv2.imread("Capture.jpg")

width = image.shape[0]
height = image.shape[1]

topLeft_XBar = customizedTrackBar(0, 1, height, 0, "x_topLeft", "Tuning Parameters")
topLeft_YBar = customizedTrackBar(0, 1, width, 0, "y_topLeft", "Tuning Parameters")

topRight_XBar = customizedTrackBar(0, 1, height, height - 1, "x_topRight", "Tuning Parameters")
topRight_YBar = customizedTrackBar(0, 1, width, 0, "y_topRight", "Tuning Parameters")

bottomRight_XBar = customizedTrackBar(0, 1, height, height - 1, "x_bottomRight", "Tuning Parameters")
bottomRight_YBar = customizedTrackBar(0, 1, width, width - 1, "y_bottomRight", "Tuning Parameters")

bottomLeft_XBar = customizedTrackBar(0, 1, height, 0, "x_bottomLeft", "Tuning Parameters")
bottomLeft_YBar = customizedTrackBar(0, 1, width, width - 1, "y_bottomLeft", "Tuning Parameters")

while True:
    topLeft = (int(topLeft_XBar.getValue()), int(topLeft_YBar.getValue()))
    topRight = (int(topRight_XBar.getValue()), int(topRight_YBar.getValue()))
    bottomRight = (int(bottomRight_XBar.getValue()), int(bottomRight_YBar.getValue()))
    bottomLeft = (int(bottomLeft_XBar.getValue()), int(bottomLeft_YBar.getValue()))
    print("start")
    print(topLeft)
    print(topRight)
    print(bottomRight)
    print(bottomLeft)

    eagleView.setDimensions(topLeft, topRight, bottomRight, bottomLeft)
    topDown = eagleView.transfrom(image)

    cloneImage = image.copy()
    cv2.line(cloneImage, topLeft, topRight, (0, 0, 255), 1)
    cv2.line(cloneImage, bottomLeft, bottomRight, (0, 0, 255), 1)
    cv2.line(cloneImage, topLeft, bottomLeft, (0, 0, 255), 1)
    cv2.line(cloneImage, bottomRight, topRight, (0, 0, 255), 1)

    cv2.imshow("Bird's Eye View", topDown)
    cv2.imshow("Original Image", cloneImage)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()