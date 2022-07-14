import cv2 as cv
from cv2 import threshold
img = cv.imread('Images/CameraTest.jpg')
cv.imshow('Test', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)

#Simple Thresholding
threshold, thresh = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)

cv.imshow('Simple Thresholded', thresh)


#Simple Thresholding
thresholdinv, thresh_inv = cv.threshold(gray, 150, 255, cv.THRESH_BINARY_INV)

cv.imshow('Simple ThresholdedINV', thresh_inv)

#Adaptive Thresholding
adaptive_thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 3)
cv.imshow('Adaptive Threshlding', adaptive_thresh)

cv.waitKey(0)