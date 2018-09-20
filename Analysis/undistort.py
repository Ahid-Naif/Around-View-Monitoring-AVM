import cv2
import numpy as np

DIM = (640, 480)
K = np.array([[2350.6, 0.0  , 314.3],
              [0.0   , 237.5, 233.2],
              [0.0   , 0.0  , 1.0  ]])
D = np.array([[0.01535], [-0.1092], [0.1003], [-0.03689]])

def undistort(image):

    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistortedImage = cv2.remap(image, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

    return undistortedImage

video = cv2.VideoCapture(1)

while True:
    isGrabbed, frame = video.read()

    clearImage = undistort(frame)

    cv2.imshow("Undistorted", clearImage)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
