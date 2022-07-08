import cv2 as cv
import numpy as np

img = cv.imread('Images/CameraTest.jpg')
cv.imshow('CameraTest', img)
b, g, r = cv.split(img)
cv.imshow('Blue', b)
cv.imshow('Green', g)
print(img.shape)
print(b.shape)
print(g.shape)

#FUN display
blank = np.zeros(img.shape[:2], dtype='uint8')
displayedBlue = cv.merge([b, blank, blank])
cv.imshow("fun Blue", displayedBlue)

merged = cv.merge([b, g, r])
cv.imshow("merged", merged)

cv.waitKey(0)