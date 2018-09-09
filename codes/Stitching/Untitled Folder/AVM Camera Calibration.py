import cv2
import numpy as np
import imutils

ix, iy = -1, -1
# mouse callback function


def draw_circle(event, x, y, flags, param):
    global ix, iy
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(Warp, (x, y), 5, (0, 0, 255), 2)
        # cv2.putText(Warp, "Point", (ix, iy), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), thickness=3)
        ix, iy = x, y
        print(ix, iy)


def warp(image, W1, W2, H1, H2):
    (h, w) = image.shape[:2]

    src = np.array([(int(w / 2) - W1, int(h / 2) - H1), (int(w/ 2) + W2, int(h / 2) - H2), (w, h), (0, h)], dtype="float32")
    dst = np.array([(0, 0), (w, 0), (int(w / 2 + 200), h), (int(w / 2 - 200), h)], dtype="float32")

    M = cv2.getPerspectiveTransform(src, dst)
    eagleEye = cv2.warpPerspective(image, M, (w, h))

    return eagleEye


def rectify(image, H11, H12, H13, H21, H22, H23, H31, H32, H33):
    # camera matrix
    K = np.array([[H11, H12, H13],
                  [H21, H22, H23],
                  [H31, H32, H33]])

    # zero distortion coefficients work well for this image
    D = np.array([0.0, 0.0, 0.0, 0.0])

    # use Knew to scale the output
    Knew = K.copy()
    Knew[(0, 1), (0, 1)] = 0.4 * Knew[(0, 1), (0, 1)]
    img_undistorted = cv2.fisheye.undistortImage(image, K, D=D, Knew=Knew)
    return img_undistorted



cv2.namedWindow('Warp')
cv2.setMouseCallback('Warp', draw_circle)
img = cv2.imread('Rear Raw.png')

Rectify = rectify(img, 522.88, 0, 601.31, 0, 771.24, 176.47, 0, 0, 1)
Warp = warp(Rectify, 221, 184, 130, 126)

newWarp = cv2.resize(Warp, (0, 0), fx=0.787, fy=0.812)

while True:

    cv2.imshow('Image', img)
    cv2.imshow('Rectify', Rectify)
    cv2.imshow('Warp', newWarp)

    if cv2.waitKey(1) == ord("q"):
        break

    elif cv2.waitKey(1) == ord("a"):
        print(ix, iy)

# cv2.imwrite('Front_TV_C.png', Warp)
# cv2.imwrite('Front_DW_C.png', Rectify)
# cv2.imwrite('Front_FE_C.png', img)
cv2.destroyAllWindows()
