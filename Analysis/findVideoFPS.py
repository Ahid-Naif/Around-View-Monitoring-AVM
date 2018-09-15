import cv2

video = cv2.VideoCapture("dataset/testVideo.mp4")
while True:
    isGrabbed, frame = video.read()

    if(not isGrabbed):
        break

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

fps = video.get(cv2.CAP_PROP_FPS)
print("fps is: {:.2f}".format(fps))
video.release()