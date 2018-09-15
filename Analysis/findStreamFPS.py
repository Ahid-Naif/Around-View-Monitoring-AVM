import cv2
import datetime

video = cv2.VideoCapture(0)

start = datetime.datetime.now()
numFrames = 0
while True:
    isGrabbed, frame = video.read()

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
    numFrames = numFrames + 1

fps = video.get(cv2.CAP_PROP_FPS)
print("fps is: {:.2f}".format(fps))
video.release()

end = datetime.datetime.now()
frameRate = numFrames/(end - start).total_seconds()
print ("Approximate fps is %(fps)d: "%{"fps": frameRate})