import cv2
import numpy as np
import glob
from myPackage.Calibration import FisheyeCalibration

fisheyeCalibration = FisheyeCalibration(6,9) 

for imagePath in glob.glob("*"):
    image = cv2.imread("imagePath")

    fisheyeCalibration.processFrame(image)
    
fisheyeCalibration.findOptimalK_D()
fisheyeCalibration.displayK_D()