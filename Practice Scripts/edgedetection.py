import cv2 as cv
img = cv.imread('Images/CameraTest')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
