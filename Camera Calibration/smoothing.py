import cv2 as cv

img = cv.imread('Images/CameraTest.jpg')
cv.imshow('Test', img)

#cv.averaging
average = cv.blur(img, (3,3))
cv.imshow('Average', average)

#Gaussian Blur
gauss = cv.GaussianBlur(img, (3, 3), 0)
cv.imshow('Gauss', gauss)

#Median Blurring (effective at reducing noise)
median = cv.medianBlur(img, 3)
cv.imshow('Median Blur', median)

#Bilateral. the 2nd param is a diameter
bilateral = cv.bilateralFilter(img, 5, 15, 15)
cv.imshow('Bilateral', bilateral)


cv.waitKey(0)