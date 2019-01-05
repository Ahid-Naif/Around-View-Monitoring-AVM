import cv2
import imutils

image = cv2.imread("BMW.jpg")
image2 = cv2.imread("mercedes.jpg")
height = image2.shape[0]

num = 30
while True:

    cv2.imshow("BMW", image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    image = imutils.translate(image, 0, num)
    image[0:num,:,:] = image2[height-1-num:height-1,:,:]