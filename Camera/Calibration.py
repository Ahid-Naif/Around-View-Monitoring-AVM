import cv2
import numpy as np

class FisheyeCalibration:
    def __init__(self, chessboardWidth, chessboardHeight, cameraName):
        """
        Following lines only define the class properties
        """
        self.chessboardDimension = (chessboardWidth, chessboardHeight)
        self.chessboardWidth = chessboardWidth
        self.chessboardHeight = chessboardHeight
        self.cameraName = cameraName
        
        """
        Following lines onle initialize variables that will be used later on
        """
        self.imageShape = None
        self.objectPoints = [] # 3d/real world coordinates - they represent the ideal pattern/corners
        self.imagePoints  = [] # 2d coordinates - they represent corners taken from camera view
        
        """
        - These two lines define the ideal internal corner in a checkerboard of any size 
        - Z coordinates are assumed to be zero to make it simple
        """
        self.idealObjectPoints = np.zeros((1, self.chessboardWidth * self.chessboardHeight, 3), np.float32)
        self.idealObjectPoints[0,:,:2] = np.mgrid[0:self.chessboardWidth, 0:self.chessboardHeight].T.reshape(-1,2)
        """
        if we have 3x3 checker board, that means, there will be 9 corners
        Thus, output/objp will be (0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2)
        """

        """
        Following lines only initilaize and define variables and flags, respectively, that will be used later on
        """
        self.subpixCriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
        self.K = np.zeros((3,3))
        self.D = np.zeros((4,1))
        self.numPoints = 0
        self.calibrationFlags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC +cv2.fisheye.CALIB_FIX_SKEW
    
    def processFrame(self, image):
        if self.imageShape == None: # if this is the 1st received image, define the variable "self.imageShape"
            self.imageShape = image.shape[0:2] # image shape is the width and height
        else:
            assert self.imageShape == image.shape[0:2] # ensure all images must have the same shape
        
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, self.chessboardDimension, cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
        if ret:
            self.objectPoints.append(self.idealObjectPoints) # store ideal corners
            corners = cv2.cornerSubPix(gray, corners, (3,3), (-1,-1), self.subpixCriteria)
            self.imagePoints.append(corners) # store detected corners
    
    def findOptimalK_D(self):
        """
        Following lines only initialize variables that will be used as arguments for cv2.fisheye.calibrate function
        """
        self.numPoints = len(self.objectPoints)
        rotationVectors = [np.zeros((1,1,3), dtype=np.float64) for i in range(self.numPoints)]
        translationVectors = [np.zeros((1,1,3), dtype=np.float64) for i in range(self.numPoints)]
        
        _, self.K, self.D, _, _ = cv2.fisheye.calibrate(
                self.objectPoints, 
                self.imagePoints, 
                self.imageShape[::-1], 
                self.K, 
                self.D, 
                rotationVectors, 
                translationVectors, 
                self.calibrationFlags, 
                (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
                )
    
    def displayK_D(self): 
        print("Found " + str(self.numPoints) + " foud images for calibration")
        print("DIM=" + str(self.imageShape[::-1]))
        print("K= (" + str(self.K.tolist()) + ")")
        print("D= (" + str(self.D.tolist()) + ")")

    def storeK_D(self):
        file = open("Parameters/K_D_Values_" + self.cameraName + ".txt", "w+") # open a new file for writing
        file.write("width  = " + str(self.imageShape[::-1][0])+"\n")
        file.write("height = " + str(self.imageShape[::-1][1])+"\n")
        
        file.write("fx = "+str(self.K[0][0])+ "\n")
        file.write("fy = "+str(self.K[1][1])+ "\n")
        file.write("cx = "+str(self.K[0][2])+ "\n")
        file.write("cy = "+str(self.K[1][2])+ "\n")

        file.write("dOne = "+str(self.D[0][0])+ "\n")
        file.write("dTwo = "+str(self.D[1][0])+ "\n")
        file.write("dThree = "+str(self.D[2][0])+ "\n")
        file.write("dFour = "+str(self.D[3][0])+ "\n")

        file.close()