import cv2

video = cv2.VideoCapture(0)

counter = 0
while True:
    isGrabbed, frame = video.read()
    if not isGrabbed:
        break

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("s"):
        counter += 1
        cv2.imwrite("dataset/Calibration/image_no_"+str(counter)+".jpg", frame)