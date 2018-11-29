import cv2
from Camera.AroundViewMonitoring import avm

frontStream = cv2.VideoCapture(0)
backStream = cv2.VideoCapture(0)

avm = avm()

while True:
    _, frontFrame = frontStream.read()
    _, backFrame = backStream.read()

    birdView = avm.runAVM(frontFrame, backFrame)
    cv2.imshow("Bird's Eye View", birdView)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()