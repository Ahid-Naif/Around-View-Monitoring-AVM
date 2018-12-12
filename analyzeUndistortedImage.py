"""
This code is used draw lines on undistorted images to evaluate the performance of unsdistortion process
"""
import cv2
import numpy as np
from Camera.Undistortion import UndistortFisheye
from TrackBar import customizedTrackBar

undistortFisheye = UndistortFisheye("Front_Camera")

while True:
    image = cv2.imread("raw.jpg")

    clearImage = undistortFisheye.undistort(image)
    cloneImage = clearImage.copy()

    gray = cv2.cvtColor(clearImage,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150)

    minLineLength = 500
    lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=minLineLength,maxLineGap=80)
    if lines is not None:
        a,b,c = lines.shape
        for i in range(a):
            cv2.line(cloneImage, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 1, cv2.LINE_AA)

    cv2.imshow("Undistorted", cloneImage)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord("r"):
        undistortFisheye.reset()

cv2.destroyAllWindows()