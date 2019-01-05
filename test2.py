import cv2
from Camera.Stitcher import stitchTwoImages

left = cv2.imread("left.png")
right = cv2.imread("right.png")
upper = cv2.imread("drogbaTop.jpg")
bottom = cv2.imread("drogabDown.jpg")

stitcher1 = stitchTwoImages("Right2Left")
stitcher2 = stitchTwoImages("Bottom2Upper")

result1 = stitcher1.stitch(right, left)
result2 = stitcher2.stitch(bottom, upper)

cv2.namedWindow("panorama1", cv2.WINDOW_NORMAL)
cv2.namedWindow("panorama2", cv2.WINDOW_NORMAL)
cv2.imshow("panorama1", result1)
cv2.imshow("panorama2", result2)
cv2.waitKey()