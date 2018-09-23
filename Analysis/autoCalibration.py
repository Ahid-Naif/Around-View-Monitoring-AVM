import cv2
import numpy as np
import glob
from myPackage.Calibration import FisheyeCalibration

calibrationFlags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_CHECK_COND +cv2.fisheye.CALIB_FIX_SKEW

#for imagePath in glob.glob("dataset/Images/Random/*"):
video = cv2.VideoCapture(0)
while True:
    isGrabbed, frame = video.read()
    if not isGrabbed:
        break
        
    fisheyeCalibration = FisheyeCalibration(6,9) 
    
    #if timer.readTimer() == 0:
     #   timer.stop()
     #   fisheyeCalibration.processFrame(frame)

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
    

    

# numPoints = len(objectPoints)
# print("Found " + str(numPoints) + " foud images for calibration")

# K = np.zeros((3,3))
# D = np.zeros((4,1))
# rotationVectors = [np.zeros((1,1,3), dtype=np.float64) for i in range(numPoints)]
# translationVectors = [np.zeros((1,1,3), dtype=np.float64) for i in range(numPoints)]

# _, K, D, _, _ = cv2.fisheye.calibrate(
#                 objectPoints, 
#                 imagePoints, 
#                 gray.shape[::-1], 
#                 K, 
#                 D, 
#                 rotationVectors, 
#                 translationVectors, 
#                 calibrationFlags, 
#                 (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
#                 )

# print("DIM=" + str(imageShape[::-1]))
# print("K= (" + str(K.tolist()) + ")")
# print("D= (" + str(D.tolist()) + ")")