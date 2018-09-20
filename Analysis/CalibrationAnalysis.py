import cv2
from myPackage.Calibration import calibrate

video = cv2.VideoCapture(1)

while True:
    isGrabbed, frame = video.read()

    if not isGrabbed:
        break
    
    calibratedImage = calibrate(frame)
    cv2.imshow("Calibrated Image", calibratedImage)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()