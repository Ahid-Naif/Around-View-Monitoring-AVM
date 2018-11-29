import cv2
from Camera.AroundViewMonitoring import avm

frontStream = cv2.VideoCapture(0)
backStream = cv2.VideoCapture(0)

avm = avm()

frontFrame = cv2.imread("Front_View.jpg")
backFrame = cv2.imread("Back_View.jpg")
frontView, backView = avm.runAVM(frontFrame, backFrame)
cv2.imshow("Front Bird's Eye View", frontView)
cv2.imshow("Back Bird's Eye View", backView)
cv2.waitKey()