import cv2
from myPackage.Calibration import calibrate

rawImage = cv2.imread("FrontRaw")

calibratedImage = calibrate(rawImage)

cv2.imshow("Calibrated Image", calibratedImage)
cv2.waitKey()