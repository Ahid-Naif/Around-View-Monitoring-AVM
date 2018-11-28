"""
This code is used to take snapshots of the chessboard which is used to calibrate  the cameras
"""
import cv2

video = cv2.VideoCapture(0)
cameraName = "Back_Camera"
chessboardDimension = (6,9)
counter = 0
while True:
    isGrabbed, frame = video.read()
    if not isGrabbed:
        break

    frameCopy = frame.copy()
    gray = cv2.cvtColor(frameCopy, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, chessboardDimension, cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
    frameCopy = cv2.drawChessboardCorners(frameCopy, chessboardDimension, corners, ret)
    cv2.imshow("Video", frameCopy)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("s"):
        counter += 1
        cv2.imwrite("Calibration_Images/"+ cameraName +"/image_no_"+str(counter)+".jpg", frame)