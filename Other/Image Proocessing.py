# import the necessary packages
import argparse
import cv2
import numpy as np
import imutils

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# load the image 
image = cv2.imread(args["image"]) # it stores the image in the object image
image.shape[0] => height
image.shape[1] => width
image.shape[2] => channel

# image show
cv2.imshow("title", <image class>)

cv2.waitKey(0) # waits for user input

#image Write
# save the image -- OpenCV handles converting filetypes
cv2.imwrite("newimage.jpg", image)

# it stores the image dimensions
(h, w) = image.shape[:2] # Multi-channel images in OpenCV are stored in row order

#drawing
# initialize our canvas as a 300x300 with 3 channels, Red, Green,
# and Blue, with a black background
canvas = np.zeros((300, 300, 3), dtype="uint8") # unit8 - number from 0 to 255

# draw a line
cv2.line(<image>, <start point -(0, 0) >,<end point - (300, 300)>, <line color - green, also can be expressed in the form (0,255,0)>, <line thicknes - not required>)

# draw a rectangle
cv2.rectangle(canvas, (50, 200), (200, 225), red, 5)

#draw a circle
cv2.circle(canvas, (centerX, centerY), radius, white)

#translation
shifted = imutils.translate(image, xShift, yShift)

#resize an image
resized = imutils.resize(image, height = 300 or width = 300) # you choose the new size of the width or the height and imutils will keep on the same ratio for you, it used INTER_AREA method by default to resize
""" interpolation methods:
	
	cv2.INTER_NEAREST + cv2.INTER_AREA => very fast, but poor quality
	cv2.INTER_LINEAR => mainly uses mathematical interpolation & good quality
	cv2.INTER_CUBIC => higher quality, but slower
"""

#rotation
rotated = imutils.rotate(image, angle, center=None, scale=1.0)

#flipping

# flip the image horizontally
flipped = cv2.flip(image, 1)
cv2.imshow("Flipped Horizontally", flipped)

# flip the image vertically
flipped = cv2.flip(image, 0)
cv2.imshow("Flipped Vertically", flipped)

# flip the image along both axes
flipped = cv2.flip(image, -1)

#cropping
# cropping an image is accomplished using simple NumPy array slices --
# let's crop the face from the image
face = image[85:250, 85:220]
cv2.imshow("Face", face)
cv2.imshow("Comparison", np.hstack([imageHarris, imageFAST]))
*******************************************************************	
#Masking
"""
Masking allows us to focus only on parts of an image that interest us.
A mask is the same size as our image, but has only two pixel values,
0 and 255. Pixels with a value of 0 are ignored in the orignal image,
"""
mask = np.zeros(image.shape[:2], dtype="uint8")
cv2.rectangle(mask, (0, 90), (290, 450), 255, -1)
cv2.imshow("Mask", mask)

# Apply out mask -- notice how only the person in the image is cropped out
masked = cv2.bitwise_and(image, image, mask=mask)
cv2.imshow("Mask Applied to Image", masked)

#Morphological operations
"""
Morphological operations are simple transformations applied to binary or grayscale images. However, there are exceptions to that, especially when using the black hat and white
hat operators

-Erosion: A foreground pixel in the input image will be kept only if ALL pixels inside the structuring element
are > 0.

-Dilation: The opposite of an erosion is a dilation. Just like an erosion will eat away at the foreground pixels, a dilation will grow the foreground pixels.

-Opening: is an erosion followed by a dilation. Performing an opening operation allows us to remove small blobs from an image, an erosion is applied to remove the small blobs, then a dilation is applied to regrow the size of the original object.

-Closing: is a dilation followed by an erosion.a closing is used to close holes inside of objects or for connecting components together.

-Morphological Gradient: is the difference between the dilation and erosion.

-Top Hat/White Hat: is difference between the original
input image and the opening. A top hat operation is used to reveal bright regions of an image on dark backgrounds. 

-Black Hat: is the difference between the closing of the input image and the input image itself.
"""
#erosion
eroded = cv2.erode(gray.copy(), None, 1)
""" 1. the image
2. None is the structuring element. If this value is None, then a 3X3 structuring element,identical to the 8-neighborhood structuring element
3. number of iterations
"""

#dilation
dilated = cv2.dilate(gray.copy(), None,1)

#Note: cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) => changes color space from BGR to GRAY scale
# cvtColor function can be used to transform from a color space into an another one.

#other operations
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, <kernelSize, i.e (3,3)>)
""" 
cv2.MORPH_RECT => to get a rectangular strucucturing element 
cv2.MORPH_CROSS => to get a 4-neighborhood structuring element
cv2.MORPH_ELLIPSE => to get a circular structuring element.
"""

cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel) # the line where morphological operation is performed
"""
cv2.MORPH_OPEN => opening
cv2.MORPH_CLOSE => closing
cv2.MORPH_GRADIENT =>  gradient # gradient is the difference between the dilation and erosion
cv2.MORPH_TOPHAT => top hat/white hat # difference between the original input image and the opening.
				      # A top hat operation is used to reveal bright regions of an image on dark backgrounds.
cv2.MORPH_BLACKHAT => black hat # difference between the closing of the input image and the input image itself.
				#Simply, it is the opposite of the white hat operator!
"""

#Smoothing & Blurring

"""
-Averaging: takes an area of pixels surrounding a central pixel, averages all these pixels together, and replaces the central pixel with the average. We are giving equal weight to all
pixels in the kernel. The larger your smoothing kernel is, the more blurred your image will look.

-Gaussian: used to remove noise that approximately follows a Gaussian distribution, where neighborhood pixels that are closer to the central pixel contribute more “weight” to the average. Furthermore, based on this weighting we’ll be able to preserve more of the edges in our image as compared to average smoothing.

-Median: unlike the averaging method, instead of replacing the central pixel with the average of the neighborhood, we instead replace the central pixel with the median of the neighborhood. Unlike average blurring and Gaussian blurring where the kernel size could be rectangular, the
kernel size for the median must be square. 

-Bilateral: In order to reduce noise while still maintaining edges, Bilateral blurring introduces two Gaussian distributions. The first Gaussian function only considers spatial neighbors. That is, pixels that appear close together in the (x, y)-coordinate space of the image. The second Gaussian then models the pixel intensity of the neighborhood, ensuring that only pixels with similar intensity are included in the actual computation of the blur.
"""
#Averaging
blurred = cv2.blur(image, <kernel size i.e. (kX, kY)>)  
#Gaussian
blurred = cv2.GaussianBlur(image, (kX, kY), 0) 
"""The last parameter is our , the standard deviation of the Gaussian distribution. By setting this value to 0, we are instructing OpenCV to automatically compute you’ll want to let your "standard deviation" become computed for you
based on our kernel size. """
#Median
blurred = cv2.medianBlur(image, k) # kernel size kxk
#Bilateral
blurred = cv2.bilateralFilter(image, diameter, sigmaColor, sigmaSpace)
"""
-diameter -the larger this diameter is, the more pixels will be included in the blurring computation. Think of this parameter as a square kernel size.
-sigmaColor is our color standard deviation. A larger value of it means that more colors in the neighborhood will be considered when computing the blur. If we let get too large in respect to the diameter, then we essentially have broken the assumption  of bilateral fltering — that only pixels of similar color should contribute signi cantly to the blur. 
-sigmaSpace is the space standard deviation. A larger value of means that pixels farther out from the central pixel diameter will in uence the blurring calculation."""

#Color spaces

# loop over each of the individual channels and display them
for (name, chan) in zip(("B/H/L", "G/S/a", "R/V/b"), cv2.split(image)):
	cv2.imshow(name, chan)

# convert the image to the HSV color space and show it
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
"""
BGR => RGB color space
HSV => HSV color space
LAB => L*a*b* color space
"""
# convert the image to the HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 

"""
COLOR_BGR2HSV
COLOR_BGR2LAB
COLOR_BGR2GRAY
"""

#Thresholding

#First, convert the image into grayscale color space. Also, apply Gaussian Distribution to remove some of the high frequency edges in the image that we are not concerned with and allow us to obtain a more “clean” segmentation.

(T, threshInv) = cv2.threshold(<image blurred>,<threshold value 200>, <output value applied during thresholding 255>, cv2.THRESH_BINARY_INV) #simple threshold
#The cv2.threshold   function then returns a tuple of 2 values: T, is the threshold value. The second returned value is the thresholded image itself.
"""
cv2.THRESH_BINARY_INV => indicates that pixel values p less than T are set to the output value (the third argument).
cv2.THRESH_BINARY => opposite if the first one
"""
(T, threshInv) = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) #Otsu's method, it finds threshold value automatically

thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, <pixel neighborhood size i.e. 25>,<to tune our threshold value i.e. 15>) #Adaptive Thresholding, it uses local thresholding (there are different threshold values for different regions of the image
"""
The third argument is the adaptive thresholding method: 
-cv2.ADAPTIVE_THRESH_MEAN_C => to indicate that we are using the arithmetic mean of the local pixel neighborhood to compute our threshold value of T.
-cv2.ADAPTIVE_THRESH_GAUSSIAN_C => usign Gaussian average instead
"""
# scikit-image adaptive thresholding, it just
thresh = threshold_adaptive(blurred, 29, offset=5).astype("uint8") * 255
thresh = cv2.bitwise_not(thresh)

#Gradients

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-l", "--lower-angle", type=float, default=175.0,
	help="Lower orientation angle")
ap.add_argument("-u", "--upper-angle", type=float, default=180.0,
	help="Upper orientation angle")
args = vars(ap.parse_args())

#Then, Convert the image into grayscale

# compute gradients along the X and Y axis, respectively
gX = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
gY = cv2.Sobel(gray, cv2.CV_64F, 0, 1)

# compute the gradient magnitude and orientation, respectively for every pixel
mag = np.sqrt((gX ** 2) + (gY ** 2))
orientation = np.arctan2(gY, gX) * (180 / np.pi) % 180

# find all pixels that are within the upper and low angle boundaries
idxs = np.where(orientation >= args["lower_angle"], orientation, -1) #In the case that the orientation is less than the minimum angle requirement, we’ll set that particular value to -1.
idxs = np.where(orientation <= args["upper_angle"], idxs, -1)
mask = np.zeros(gray.shape, dtype="uint8")
mask[idxs > -1] = 255 #all coordinates that have a corresponding idxs   value of > -1 are set to 255 (i.e. foreground). Otherwise, they are left as 0 (i.e. background).

# -Extra Operations-
# the `gX` and `gY` images are now of the floating point data type,
# so we need to take care to convert them back a to unsigned 8-bit
# integer representation so other OpenCV functions can utilize them
gX = cv2.convertScaleAbs(gX)
gY = cv2.convertScaleAbs(gY)

# combine the sobel X and Y representations into a single image
sobelCombined = cv2.addWeighted(gX, 0.5, gY, 0.5, 0)

#Edge Detection

#First, we blurr the image, then, we convert it into grayscale color space
#then,
# compute a "wide", "mid-range", and "tight" threshold for the edges
wide = cv2.Canny(blurred, 10, 200)
mid = cv2.Canny(blurred, 30, 150)
tight = cv2.Canny(blurred, 240, 250)
#We can compare the three of them. Using this way, we can manually adjust the upper and lower level of the edges thresholds. However, most of the times, we will use auto_canny which sets the thresholds values mainly based on the median of pixels intensities.
auto = imutils.auto_canny(blurred, sigma=0.33)) # sigma is an optional argument

#contours

#First, convert the image into grayscale
# find all contours in the image and draw ALL contours on the image
(cnts, _) = cv2.findContours(gray.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
"""
cv2.RETR_LIST => to return a list of all contours in the image
cv2.RETR_EXTERNAL => to return only external contours
cv2.CHAIN_APPROX_SIMPLE => to store compressed version of the contour to save memory
"""
#to draw found contours
cv2.drawContours(clone, cnts, -1, (0, 255, 0), 2)
"""
-1 => to print all the contours
(0,255,0) -green => color of printed contour
2 => contour thickness
"""
"""
Drawing the first two contours:
cv2.drawContours(clone, cnts[:2], -1, (0, 255, 0), 2)
"""
#re-clone the image and close all open windows
clone = image.copy() #to get the original image
#Contours with masks:-
mask = np.zeros(gray.shape, dtype="uint8")
cv2.drawContours(mask, [c], -1, 255, -1)
 
# show the images
cv2.imshow("Image", image)
cv2.imshow("Mask", mask)
cv2.imshow("Image + Mask", cv2.bitwise_and(image, image, mask=mask))
#-------------------------------------

#Contours properties:-

#Centroid/Center of Mass
for c in cnts:
# compute the moments of the contour which can be used to compute the
# centroid or "center of mass" of the region
M = cv2.moments(c)
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
 
# draw the center of the contour on the image
cv2.circle(clone, (cX, cY), 10, (0, 255, 0), -1)

#Area
area = cv2.contourArea(c)
#Perimeter
perimeter = cv2.arcLength(c, True) # "True" refers to that the contour is closed
#Bounding Boxes
(x, y, w, h) = cv2.boundingRect(c)
cv2.rectangle(clone, (x, y), (x + w, y + h), (0, 255, 0), 2)
#Rotated Bounding Boxes
box = cv2.minAreaRect(c)
box = np.int0(cv2.cv.BoxPoints(box))
cv2.drawContours(clone, [box], -1, (0, 255, 0), 2)
#Minimum Enclosing Circles
((x, y), radius) = cv2.minEnclosingCircle(c)
cv2.circle(clone, (int(x), int(y)), int(radius), (0, 255, 0), 2)
#Fitting an Ellipse
for c in cnts:
# to fit an ellipse, our contour must have at least 5 points
if len(c) >= 5:
# fit an ellipse to the contour
ellipse = cv2.fitEllipse(c)
cv2.ellipse(clone, ellipse, (0, 255, 0), 2)
#Aspect Ratio
aspect ratio = image width / image height
#Extent
extent = shape area / bounding box area
extent = area / float(w * h)
#Convex Hull
Convex Hull is enclosing polygon of all points of the input shape
hull = cv2.convexHull(c)
#Solidity
solidity = contour area / convex hull area
hullArea = cv2.contourArea(hull)

#Contour Approximation
"""contour approximation is an algorithm for reducing the number of points in a
curve with a reduced set of points"""
for c in cnts:
# approximate the contour
peri = cv2.arcLength(c, True)
approx = cv2.approxPolyDP(c, 0.01 * peri, True)
# if the approximated contour has 4 vertices, then we are examining
# a rectangle
if len(approx) == 4:
# draw the outline of the contour and draw the text on the image
cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
(x, y, w, h) = cv2.boundingRect(approx)
cv2.putText(image, "Rectangle", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

#read approx_realworld.py
#-------------------------------------

#Historams

#A histogram represents the distribution of pixel intensities (whether color or gray- scale) in an image.
cv2.calcHist(images, channels, mask, histSize, ranges)
"""
-images: This is the image that we want to compute a histogram for. Wrap it as a list: [myImage].
-channels: A list of indexes, where we specify the index of the channel we want to compute a histogram for. To compute a histogram of a grayscale image, the list would be [0]  . To compute a
histogram for all three red, green, and blue channels, the channels list would be [0, 1, 2].
-mask: to be able to calculate a histogram for a masked area. Make it "None" if there's no mask to be applied.
-histSize: This is the number of bins we want to use when computing a histogram. Again, this is a
list, one for each channel we are computing a histogram for. The bin sizes do not all have to be the same. Here is an example of 32 bins for each channel: [32, 32, 32].
-ranges: The range of possible pixel values. Normally, this is [0, 256] (this is not a typo — the
ending range of the cv2.calcHist function is non-inclusive so you’ll want to provide a value of
256 rather than 255) for each channel, but if you are using a color space other than RGB [such as
HSV], the ranges might be different.)
"""
from matplotlib import pyplot as plt
# construct a grayscale histogram
hist = cv2.calcHist([image], [0], None, [256], [0, 256])  
# plot the histogram
plt.figure()
plt.title("Grayscale Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")
plt.plot(hist)
plt.xlim([0, 256])

# histogram normalization
hist /= hist.sum()

#Color Histograms
#read color_histograms.py

#Histogram Equalization
#Applying histogram equalization will stretch the peak out towards the corner of the image, thus improving the global contrast of the image. Histogram equalization is applied to grayscale images.

eq = cv2.equalizeHist(image)

#Color Channel Statistics
#read color_channel_stats.py

#Color histograms as image descriptors
#Read the file





