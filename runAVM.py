import cv2
from Camera.AroundViewMonitoring import avm
import datetime


# frontStream = cv2.VideoCapture(0)
# backStream = cv2.VideoCapture(1)
frontStream = cv2.VideoCapture("front_camera.avi")
backStream = cv2.VideoCapture("back_camera.avi")

avm = avm()

# frontFrame = cv2.imread("Front_View.jpg")
# backFrame = cv2.imread("Back_View.jpg")
startTime = datetime.datetime.now()
while True:
    isGrabbed, frontFrame = frontStream.read()
    isGrabbed2, backFrame = backStream.read()
    if not isGrabbed or not isGrabbed2:
        break

    birdView = avm.runAVM(frontFrame, backFrame)
    cv2.imshow("Bird's Eye View", birdView)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
endTime = datetime.datetime.now()
time = (endTime - startTime).total_seconds()
print ("Approximate elapsed time is %(fps)d: "%{"fps": time})
cv2.destroyAllWindows()