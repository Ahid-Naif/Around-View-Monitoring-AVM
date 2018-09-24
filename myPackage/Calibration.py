import cv2
import numpy as np

class FisheyeCalibration:
    def __init__(self, width, height):
        self.imageShape = None
        self.objectPoints = [] # 3d/real world coordinates
        self.imagePoints  = [] # 2d coordinates
        self.checkerboardDimension = (width, height)
        """
        / These two lines define the ideal internal corner in a checkerboard of any size 
        / Z coordinates are assumed to be zero to make it simple
        """
        self.idealObjectPoints = np.zeros((1, self.checkerboardDimension[0]*self.checkerboardDimension[1], 3), np.float32)
        self.idealObjectPoints[0,:,:2] = np.mgrid[0:self.checkerboardDimension[0], 0:self.checkerboardDimension[1]].T.reshape(-1,2)
        """
        if we have 3x3 checker board, that means, there will be 9 corners
        Thus, output/objp will be (0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (0,2), (1,2), (2,2)
        """
        self.subpixCriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
        self.K = np.zeros((3,3))
        self.D = np.zeros((4,1))
        self.numPoints = 0
        self.calibrationFlags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_CHECK_COND +cv2.fisheye.CALIB_FIX_SKEW
    
    def processFrame(self, image):
        if self.imageShape == None:
            self.imageShape = image.shape[0:2]
        else:
            assert self.imageShape == image.shape[0:2] # all images must have the same shape
        
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, self.checkerboardDimension, cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
        if ret:
            self.objectPoints.append(self.idealObjectPoints)
            corners = cv2.cornerSubPix(gray, corners, (3,3), (-1,-1), self.subpixCriteria)
            self.imagePoints.append(corners)
    
    def findOptimalK_D(self):
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
        file = open("K_D_Values.txt", "w+")
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

    def calibrate(self, img):

        H11 = 2350.6
        H12 = 0
        H13 = 314.3
        H21 = 0
        H22 = 237.5
        H23 = 233.2
        H31 = 0.0
        H32 = 0.0
        H33 = 1.0

        K = np.array([[H11, H12, H13],
                    [H21, H22, H23],
                    [H31, H32, H33]])

        D = np.array([[0.01535], [-0.1092], [0.1003], [-0.03689]]) # ignore distortion vector for the moment

        Knew = np.identity(3, dtype=float)

        undistortedImage = cv2.fisheye.undistortImage(img, K, D=D, Knew=Knew) # how does work?

        return undistortedImage

