import cv2
import numpy as np

def doNothing(_):
    pass

image = np.zeros((300, 300, 3), dtype=np.uint8)
cv2.namedWindow("image")

cv2.createTrackbar("R", "image", 0, 255, doNothing)
cv2.createTrackbar("G", "image", 0, 255, doNothing)
cv2.createTrackbar("B", "image", 0, 255, doNothing)

cv2.setTrackbarPos("R", "image", 100)
cv2.setTrackbarPos("G", "image", 100)
cv2.setTrackbarPos("B", "image", 100)

while True:
    cv2.imshow("image", image)

    R = cv2.getTrackbarPos("R", "image")
    G = cv2.getTrackbarPos("G", "image")
    B = cv2.getTrackbarPos("B", "image")

    image[:] = [B, G, R]

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()


