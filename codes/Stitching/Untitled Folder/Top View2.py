import cv2
import numpy as np
import imutils


def getValue(value):
    return value


cv2.namedWindow('T', cv2.WINDOW_NORMAL)
cv2.createTrackbar('H11', 'T', 0, 1000000, getValue)
cv2.createTrackbar('H12', 'T', 0, 100000, getValue)
cv2.createTrackbar('H13', 'T', 0, 100000, getValue)
cv2.createTrackbar('H21', 'T', 0, 100000, getValue)
cv2.createTrackbar('H22', 'T', 0, 100000, getValue)
cv2.createTrackbar('H23', 'T', 0, 100000, getValue)
cv2.createTrackbar('H31', 'T', 0, 100000, getValue)
cv2.createTrackbar('H32', 'T', 0, 100000, getValue)
cv2.createTrackbar('H33', 'T', 0, 100000, getValue)
cv2.createTrackbar('1', 'T', 0, 100, getValue)
cv2.createTrackbar('2', 'T', 0, 100, getValue)
cv2.createTrackbar('3', 'T', 0, 100, getValue)
cv2.createTrackbar('4', 'T', 0, 100, getValue)
cv2.createTrackbar('W1', 'T', 0, 300, getValue)
cv2.createTrackbar('W2', 'T', 0, 300, getValue)
cv2.createTrackbar('H1', 'T', 0, 300, getValue)
cv2.createTrackbar('H2', 'T', 0, 300, getValue)

cv2.setTrackbarPos('H11', 'T', 43752)
cv2.setTrackbarPos('H12', 'T', 0)
cv2.setTrackbarPos('H13', 'T', 60131)
cv2.setTrackbarPos('H21', 'T', 0)
cv2.setTrackbarPos('H22', 'T', 59477)
cv2.setTrackbarPos('H23', 'T', 28758)
cv2.setTrackbarPos('H31', 'T', 0)
cv2.setTrackbarPos('H32', 'T', 0)
cv2.setTrackbarPos('H33', 'T', 100)
cv2.setTrackbarPos('W1', 'T', 180)
cv2.setTrackbarPos('W2', 'T', 180)
cv2.setTrackbarPos('H1', 'T', 100)
cv2.setTrackbarPos('H2', 'T', 100)

#cv2.setTrackbarPos('H11', 'T', 52288)
#cv2.setTrackbarPos('H12', 'T', 0)
#cv2.setTrackbarPos('H13', 'T', 62092)
#cv2.setTrackbarPos('H21', 'T', 0)
#cv2.setTrackbarPos('H22', 'T', 84314)
#cv2.setTrackbarPos('H23', 'T', 31373)
#cv2.setTrackbarPos('H31', 'T', 0)
#cv2.setTrackbarPos('H32', 'T', 0)
#cv2.setTrackbarPos('H33', 'T', 100)

ix, iy = -1, -1
# mouse callback function


def draw_circle(event, x, y, flags, param):
    global ix, iy
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img, (x, y), 3000, (0, 255, 0), -1)
        ix, iy = x, y
        print(ix, iy)


def warp(image):
    (h, w) = image.shape[:2]

    W1 = cv2.getTrackbarPos('W1', 'T')
    W2 = cv2.getTrackbarPos('W2', 'T')
    H1 = cv2.getTrackbarPos('H1', 'T')
    H2 = cv2.getTrackbarPos('H2', 'T')

    src = np.array([(int(w / 2) - W1, int(h / 2) - H1), (int(w/ 2) + W2, int(h / 2) - H2), (w, h), (0, h)], dtype="float32")
    dst = np.array([(0, 0), (w, 0), (int(w / 2 + 200), h), (int(w / 2 - 200), h)], dtype="float32")

    M = cv2.getPerspectiveTransform(src, dst)
    eagleEye = cv2.warpPerspective(image, M, (w, h))

    return eagleEye


def rectify(image):
    H11 = cv2.getTrackbarPos('H11', 'T')
    H12 = cv2.getTrackbarPos('H12', 'T')
    H13 = cv2.getTrackbarPos('H13', 'T')
    H21 = cv2.getTrackbarPos('H21', 'T')
    H22 = cv2.getTrackbarPos('H22', 'T')
    H23 = cv2.getTrackbarPos('H23', 'T')
    H31 = cv2.getTrackbarPos('H31', 'T')
    H32 = cv2.getTrackbarPos('H32', 'T')
    H33 = cv2.getTrackbarPos('H33', 'T')

    K = np.array([[H11 / 100, H12 / 100, H13 / 100],
                  [H21 / 100, H22 / 100, H23 / 100],
                  [H31 / 100, H32 / 100, 1]])

    # zero distortion coefficients work well for this image
    f1 = cv2.getTrackbarPos('1', 'T')
    f2 = cv2.getTrackbarPos('2', 'T')
    f3 = cv2.getTrackbarPos('3', 'T')
    f4 = cv2.getTrackbarPos('4', 'T')

    D = np.array([f1 / 100, f2 / 100, f3 / 100, f4 / 100])

    # use Knew to scale the output
    Knew = K.copy()
    Knew[(0, 1), (0, 1)] = 0.4 * Knew[(0, 1), (0, 1)]

    img_undistorted = cv2.fisheye.undistortImage(image, K, D=D, Knew=Knew)
    return img_undistorted


# cap = cv2.VideoCapture('front test 4.avi')
cv2.namedWindow('Warp')
cv2.setMouseCallback('Warp', draw_circle)

while True:
    img = cv2.imread('rear raw.png')
    # _, img = cap.read()
    # img = imutils.resize(img, width=1200)
    Rectify = rectify(img)
    Warp = warp(Rectify)
    cv2.imshow('Image', img)
    cv2.imshow('Rectify', Rectify)
    cv2.imshow('Warp', Warp)

    if cv2.waitKey(1) == ord("q"):
        break

    elif cv2.waitKey(1) == ord("a"):
        print(ix, iy)

cv2.destroyAllWindows()
