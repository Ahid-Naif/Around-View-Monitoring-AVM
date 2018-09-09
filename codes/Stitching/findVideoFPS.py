import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, help="Path to the video file")
args = vars(ap.parse_args())

video = cv2.VideoCapture(args["video"])
while True:
    isGrabbed, frame = video.read()

    if(not isGrabbed):
        break

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


fps = video.get(cv2.CAP_PROP_FPS);
print("fps is: {:.2f}".format(fps))
video.release()