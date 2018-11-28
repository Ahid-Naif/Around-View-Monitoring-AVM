"""
This code usese the output imaegs of takeSnapshots.py code to calibrate the fisheye camera
"""
import cv2
from imutils import paths
from Camera.Calibration import FisheyeCalibration

chessboardDimension = (6,9)
width = chessboardDimension[0]
height = chessboardDimension[1]
cameraName = "Front_Camera"
fisheyeCalibration = FisheyeCalibration(width, height, cameraName)

imagesPaths = list(paths.list_images("Calibration_Images" + cameraName))
for imagePath in imagesPaths:
    image = cv2.imread(imagePath)
    
    fisheyeCalibration.processFrame(image)
    
fisheyeCalibration.findOptimalK_D()
fisheyeCalibration.displayK_D()
fisheyeCalibration.storeK_D()