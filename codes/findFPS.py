# the purpose of this code is to find fps
# so that we can figure out how does each detector/descriptor affect on fps rate
import cv2
import datetime
from myPackage.KeyPointDetectors import detectKeypoints
from myPackage.KeyPointsDescriptors import computeKeypoints


video = cv2.VideoCapture(0)

start = datetime.datetime.now()
numFrames = 0
while True:
    isGrabbed, frame = video.read()

    ORB = detectKeypoints(frame)
    outputImage, keypoints = ORB.detectORB(True)
    descriptor = computeKeypoints(frame, keypoints)
    kps, des = descriptor.computeSURF()

    cv2.imshow("Video", outputImage)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
    numFrames += 1

fps = video.get(cv2.CAP_PROP_FPS)
print("fps is: {:.2f}".format(fps))
video.release()

end = datetime.datetime.now()
frameRate = numFrames/(end - start).total_seconds()
print ("Approximate fps is %(fps)d: "%{"fps": frameRate})