import cv2
import numpy as np
import imutils


fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('Stadium.avi', fourcc, 20.0, (951, 625))


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

cv2.setTrackbarPos('H11', 'T', 26144)
cv2.setTrackbarPos('H12', 'T', 0)
cv2.setTrackbarPos('H13', 'T', 63399)
cv2.setTrackbarPos('H21', 'T', 0)
cv2.setTrackbarPos('H22', 'T', 59477)
cv2.setTrackbarPos('H23', 'T', 21579)
cv2.setTrackbarPos('H31', 'T', 0)
cv2.setTrackbarPos('H32', 'T', 0)
cv2.setTrackbarPos('H33', 'T', 100)
cv2.setTrackbarPos('W1', 'T', 180)
cv2.setTrackbarPos('W2', 'T', 180)
cv2.setTrackbarPos('H1', 'T', 100)
cv2.setTrackbarPos('H2', 'T', 100)


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


vs1 = cv2.VideoCapture('Front Test 7.avi')
vs2 = cv2.VideoCapture('Rear Test 7.avi')
_, front = vs1.read()
(h, w) = front.shape[:2]
canvas = np.zeros((h * 2, w, 3), dtype=np.uint8)
temp = np.zeros((12 * h, w, 3), dtype=np.uint8)
Out = np.zeros((625, 951, 3), dtype=np.uint8)
i = 0
j = 0

while True:
    _, front = vs1.read()
    _, rear = vs2.read()

    frameNo = int(vs1.get(cv2.CAP_PROP_POS_FRAMES))
    total = int(vs1.get(cv2.CAP_PROP_FRAME_COUNT))

    Rf = rectify(front)
    Wf = warp(Rf)
    Rr = rectify(rear)
    Wr = warp(Rr)
    Wrr = imutils.rotate_bound(Wr, 180)

    resizedF = imutils.resize(front, height=310)
    resizedR = imutils.resize(rear, height=310)

    canvas[:h, :] = Wf[:, :]
    canvas[h:, :] = Wrr[:, :]

    temp[temp.shape[0] - 2000 - int(h / 2) - i:temp.shape[0] - 2000 - i, :] = Wf[:int(h / 2), :]
    i = i + 25

    crop = temp.copy()
    Crop = crop[crop.shape[0] - 2000 - j:crop.shape[0] - j, :]
    j = j + 28

    Crop[:int(h / 2), :] = Wf[:int(h / 2), :]
    Crop[Crop.shape[0] - int(h / 2):, :] = Wrr[int(h / 2):, :]

    resized = imutils.resize(canvas, height=700)
    resizedTemp = imutils.resize(temp, width=400)
    resizedCrop = imutils.resize(Crop, width=400)

    Out[:, :400] = resizedCrop[:, :]
    Out[:resizedF.shape[0], 400:] = resizedF[:, :]
    Out[resizedF.shape[0] + 5:, 400:] = resizedR[:, :]

    # out.write(Out)

    print(resizedCrop.shape[:2], resizedF.shape[:2], frameNo, total)

    if frameNo == 200:
        cv2.imwrite('frame200.png', Wf)

    elif frameNo == 201:
        cv2.imwrite('frame201.png', Wf)

    elif frameNo == 205:
        cv2.imwrite('frame205.png', Wf)

    cv2.imshow('Front', Wf)
    cv2.imshow('Rear', Wrr)
    cv2.imshow('Canvas', resizedCrop)
    cv2.imshow('Temp', resizedTemp)
    cv2.imshow('Out', Out)

    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
