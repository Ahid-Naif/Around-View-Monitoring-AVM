import cv2
import numpy as np
import glob

CHECKERBOARD = (6,9)
subpixCriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
Image = cv2.imread("checkerboard")
calibrationFlags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_CHECK_COND +cv2.fisheye.CALIB_FIX_SKEW

"""
/ These two lines define the ideal internal corner in a checkerboard of any size 
/ Z coordinates are assumed to be zero to make it simple
"""
objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1,2)
"""
if we have 3x3 checker board, that means, therewe have 9 corners
Thus, output will be (0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2)
"""

imageShape = None
objectPoints = [] # 3d/real world coordinates
imagePoints  = [] # 2d coordinates

images = glob.glob('*.jpg')

for filePath in images:
    image = cv2.imread(filePath)

    if imageShape == None:
        imageShape = image.shape[0:2]
    else:
        assert imageShape == image.shape[0:2] # all images must have the same shape
    
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
    if ret:
        objectPoints.append(objp)
        corners = cv2.cornerSubPix(gray, corners, (3,3), (-1,-1), subpixCriteria)
        imagePoints.append(corners)

numPoints = len(objectPoints)
K = np.zeros((3,3))
D = np.zeros((4,1))
rotationVectors = [np.zeros((1,1,3), dtype=np.float64) for i in range(numPoints)]
translationVectors = [np.zeros((1,1,3), dtype=np.float64) for i in range(numPoints)]

_, K, D, _, _ = cv2.fisheye.calibrate(
                objectPoints, 
                imagePoints, 
                gray.shape[::-1], 
                K, 
                D, 
                rotationVectors, 
                translationVectors, 
                calibrationFlags, 
                (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
                )

print("DIM=" + str(imageShape[::-1]))
print("K= (" + str(K.tolist()) + ")")
print("D= (" + str(D.tolist()) + ")")