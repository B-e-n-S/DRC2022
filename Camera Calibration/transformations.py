import cv2 as cv
import numpy as np

#Works for live video, files or non-live.
def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

img = cv.imread('Images/Cat.jpg')
img = rescaleFrame(img, scale=0.4)

# Translation (x pixels or y pixels)
def translate(img, x, y): 
    transMat = np.float32([[1,0,x], [0,1,y]])
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, transMat, dimensions)
# -x --> shift Left (i.e. positive x shifts right)
# -y --> shift Up (i.e. positive y shifts down)

translated = translate(img, -100, 100)
cv.imshow('Translated', translated)

# Rotation
def rotate(img, angle, rotPoint=None) :
    (height, width) = img.shape[:2]

    if rotPoint is None:
        rotPoint = (width//2, height//2) #i.e. rotation about centre

    rotMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
    dimensions = (width, height)
    return cv.warpAffine(img, rotMat, dimensions)    

rotated = rotate(img, 45)
#cv.imshow("Rotated", rotated)
#cv.imshow("Rotated again", rotate(rotated, 45))

#Resizing
resized = cv.resize(img, (500, 500), interpolation=cv.INTER_AREA)

#Flipping
flip =cv.flip(img, 0) #0 is flip vertically, 1 is horizontally and -1 is both
cv.imshow("flip", flip)

#Cropping
cropped = img[200:400, 300:400]
#cv.imshow("cropped", cropped)

cv.waitKey(0)