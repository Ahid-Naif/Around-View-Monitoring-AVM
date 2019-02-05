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
fisheyeCalibration = FisheyeCalibration(width, height, cameraName) # initilize an object of FisheyeCalibration class

imagesPaths = list(paths.list_images("Calibration_Images/" + cameraName)) # store all pahts of images in the sirectory
for imagePath in imagesPaths: # read paths one by one
    image = cv2.imread(imagePath) # read images one by one
    
    fisheyeCalibration.processFrame(image) # process images one by one for calibration
    
fisheyeCalibration.findOptimalK_D()
fisheyeCalibration.displayK_D()
fisheyeCalibration.storeK_D()