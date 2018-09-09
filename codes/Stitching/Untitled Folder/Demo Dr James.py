import cv2
import imutils
import numpy as np


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

cv2.createTrackbar('W1', 'T', 0, 300, getValue)
cv2.createTrackbar('W2', 'T', 0, 300, getValue)
cv2.createTrackbar('H1', 'T', 0, 300, getValue)
cv2.createTrackbar('H2', 'T', 0, 300, getValue)
cv2.createTrackbar('W3', 'T', 0, 300, getValue)
cv2.createTrackbar('W4', 'T', 0, 300, getValue)
cv2.createTrackbar('H3', 'T', 0, 300, getValue)

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
cv2.setTrackbarPos('W3', 'T', 200)
cv2.setTrackbarPos('W4', 'T', 200)
cv2.setTrackbarPos('H3', 'T', 0)


def warp(image, rotate, flip, H11, H13, H22, H23, W1, H1):
    image = imutils.resize(image, width=1200)
    rectifyImage = rectify(image, H11, H13, H22, H23)
    (h, w) = rectifyImage.shape[:2]

    # W1 = cv2.getTrackbarPos('W1', 'T')
    # W2 = cv2.getTrackbarPos('W2', 'T')
    # H1 = cv2.getTrackbarPos('H1', 'T')
    # H2 = cv2.getTrackbarPos('H2', 'T')
    # W3 = cv2.getTrackbarPos('W3', 'T')
    # W4 = cv2.getTrackbarPos('W4', 'T')
    # H3 = cv2.getTrackbarPos('H3', 'T')
    H3 = 0
    W3 = 200
    W4 = 200

    src = np.array([(int(w / 2) - W1, int(h / 2) - H1), (int(w / 2) + W1, int(h / 2) - H1), (w, h - H3), (0, h - H3)], dtype="float32")
    dst = np.array([(0, 0), (w, 0), (int(w / 2 + W3), h), (int(w / 2 - W4), h)], dtype="float32")

    M = cv2.getPerspectiveTransform(src, dst)
    eagleEye = cv2.warpPerspective(rectifyImage, M, (w, h))

    eagleEye = imutils.rotate_bound(eagleEye, rotate)
    eagleEye = cv2.flip(eagleEye, flip)

    return rectifyImage, eagleEye


def rectify(image, H11, H13, H22, H23):
    # H11 = cv2.getTrackbarPos('H11', 'T')
    # H12 = cv2.getTrackbarPos('H12', 'T')
    # H13 = cv2.getTrackbarPos('H13', 'T')
    # H21 = cv2.getTrackbarPos('H21', 'T')
    # H22 = cv2.getTrackbarPos('H22', 'T')
    # H23 = cv2.getTrackbarPos('H23', 'T')
    # H31 = cv2.getTrackbarPos('H31', 'T')
    # H32 = cv2.getTrackbarPos('H32', 'T')
    # H33 = cv2.getTrackbarPos('H33', 'T')

    K = np.array([[H11 / 100, 0.        , H13 / 100],
                  [0.       , H22 / 100 , H23 / 100],
                  [0.       , 0.        , 1.       ]])

    # zero distortion coefficients work well for this image
    D = np.array([0., 0., 0., 0.])

    # use Knew to scale the output
    Knew = K.copy()
    Knew[(0, 1), (0, 1)] = 0.4 * Knew[(0, 1), (0, 1)]

    img_undistorted = cv2.fisheye.undistortImage(image, K, D=D, Knew=Knew)
    return img_undistorted


def paste(i, j):
    (h, w) = WarpB.shape[:2]
    # print(h, w)

    # canvas[:100, :] = \
    #    WarpA[int(h / 2) + 50:int(h / 2) + 150, int(w / 2) - 300:int(w / 2) + 300]

    newCanvas[500 + i:600 + i, :] = \
        WarpB[80:180, int(w / 2) - 300:int(w / 2) + 300]

    Crop = newCanvas.copy()
    Crop = Crop[j:700 + j, :]

    Crop[Crop.shape[0] - 100:, :] = \
        WarpB[170:270, int(w / 2) - 300:int(w / 2) + 300]

    Crop[:100, :] = \
        WarpA[WarpA.shape[0] - 250:WarpA.shape[0] - 150, int(WarpA.shape[1] / 2) - 300:int(WarpA.shape[1] / 2) + 300]

    print(car.shape[:3], Crop.shape[:3], i)

    Final = cv2.addWeighted(Crop, 1, car, 1, 0)

    return WarpA, WarpB, Final


def stitch(images, ratio=0.75, reprojThresh=4.0, showMatches=False):
    (imageB, imageA) = images
    (kpsA, featuresA) = detect(imageA)
    (kpsB, featuresB) = detect(imageB)

    M = match(kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh)

    if M is None:
        return None

    (matches, H, status) = M
    result = cv2.warpPerspective(imageA, H, (imageA.shape[1], imageA.shape[0] + imageB.shape[0]))
    result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

    if showMatches:
        # vis = draw(imageA, imageB, kpsA, kpsB, matches, status)
        return result

    return result


def preProcessing(frame, translate, angle):
    return frame


def detect(image):
    descriptor = cv2.xfeatures2d.SIFT_create()
    (kps, features) = descriptor.detectAndCompute(image, None)
    kps = np.float32([kp.pt for kp in kps])

    return kps, features


def match(kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh):
    matcher = cv2.DescriptorMatcher_create("BruteForce")
    rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
    matches = []

    for m in rawMatches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            matches.append((m[0].trainIdx, m[0].queryIdx))

    if len(matches) > 4:
        ptsA = np.float32([kpsA[i] for (_, i) in matches])
        ptsB = np.float32([kpsB[i] for (i, _) in matches])
        (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)

        return matches, H, status

    return None


def draw(imageA, imageB, kpsA, kpsB, matches, status):
    (hA, wA) = imageA.shape[:2]
    (hB, wB) = imageB.shape[:2]
    vis = np.zeros((hA + hB, max(wA, wB), 3), dtype="uint8")
    vis[0:hA, 0:wA] = imageA
    vis[hA:2*hA, 0:wA] = imageB

    for ((trainIdx, queryIdx), s) in zip(matches, status):
        if s == 1:
            ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
            ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
            cv2.line(vis, ptA, ptB, (0, 255, 0), 1)

    return vis


capA = cv2.VideoCapture('frontView.mp4')
capB = cv2.VideoCapture('rearView.mp4')
canvas = np.zeros((800, 600, 3), dtype=np.uint8)
newCanvas = np.zeros((2050, 600, 3), dtype=np.uint8)
car = cv2.imread('car2.jpg')
i = 0
j = 0


while True:
    _, frameA = capA.read()
    _, frameB = capB.read()

    frameNo = int(capB.get(cv2.CAP_PROP_POS_FRAMES))

    (RectifyA, WarpA) = warp(frameA, 180, 0, 45752, 62092, 75163, 28105, 137, 158)
    (RectifyB, WarpB) = warp(frameB, 180, 1, 43752, 60784, 59477, 34641, 142, 100)

    print(RectifyA.shape[:2], RectifyB.shape[:2])

    Out = np.zeros(((RectifyA.shape[0] + RectifyB.shape[0]), RectifyA.shape[1], 3), dtype=np.uint8)

    Out[:RectifyA.shape[0], :] = WarpA[:, :]
    Out[RectifyA.shape[0]:, :] = WarpB[:, :]
    Out = imutils.resize(Out, height=600)

    # (WarpA, WarpB, Final) = paste(i, j)
    # i = i + 6
    # j = j + 6

########################################################################################################################
    # Optional, Unstable
    
    # if (frameNo % 3) == 0:
    #    (WarpA) = stitch([WarpA, WarpB], showMatches=True)

    cv2.imshow('Front', RectifyA)
    cv2.imshow('Rear', RectifyB)
    cv2.imshow('Crop', Out)

    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
