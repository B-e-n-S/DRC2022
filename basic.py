import cv2 as cv


#Works for live video, files or non-live.
def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

img = cv.imread('Images\CameraTest.jpg')
img = rescaleFrame(img, scale=0.45)

#Converting to grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#cv.imshow('Gray', gray)

#Blur image
blur = cv.GaussianBlur(img, (3, 3), cv.BORDER_DEFAULT)
cv.imshow('Blur', blur)

#Edge Cascade
canny = cv.Canny(img, 125, 175)
cv.imshow('Canny Edges default', canny)
cannyblur = cv.Canny(blur, 125, 175)
cv.imshow('Canny Edges', canny)

cv.waitKey(0)