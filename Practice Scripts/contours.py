import cv2 as cv
import numpy as np

# #Works for live video, files or non-live.
# def rescaleFrame(frame, scale=0.75):
#     width = int(frame.shape[1] * scale)
#     height = int(frame.shape[0] * scale)
#     dimensions = (width, height)
#     return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

# img = cv.imread('Images/Cat.jpg')
# img2 = rescaleFrame(img, scale=0.4)

# gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
# # gray= cv.GaussianBlur(gray, (3,3), cv.BORDER_DEFAULT)
# cv.imshow('Gray', gray)

# blank = np.zeros(gray.shape, dtype='uint8')
# #cv.imshow("blank", blank)
# # canny = cv.Canny(gray, 125, 175)
# # cv.imshow('Canny Edges', canny)

# #Alt method:
# ret, thresh = cv.threshold(gray, 125, 255, cv.THRESH_BINARY)
# cv.imshow("Thresholded image", thresh)
# #RETR_LIST returns all the countours.
# # Returns python list of all coordinates of coordinates found in the list. Hierachies is representation of contours. 
# # E.g. if have circle in sfquare in rectangle. 
# #RETR_LIST returns all of the contours. RETR_EXTERNAL returns all those on the outside.
# #RETR_HEIRACHICAL returns all those in a heirachy.
# #CHAIN_APPROX_SIMPLE, simplifies the contours (takes all the points and simplifies line into two end points)
# contours, hierachies = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
# print(f'{len(contours)} contour(s) found')
# cv.drawContours(blank, contours, -1, (0, 0, 255), 2)
# cv.imshow('Contours Drawn', blank)

img = cv.imread('Images/CameraTest.jpg')
cv.imshow('Test', img)

blank = np.zeros(img.shape, dtype='uint8')
cv.imshow('Blank', blank)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)

blur = cv.GaussianBlur(gray, (5,5), cv.BORDER_DEFAULT)
cv.imshow('Blur', blur)

# canny = cv.Canny(blur, 125, 175)
# cv.imshow('Canny Edges', canny)

ret, thresh = cv.threshold(gray, 125, 255, cv.THRESH_BINARY)
cv.imshow('Thresh', thresh)

contours, hierarchies = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
print(f'{len(contours)} contour(s) found!')

cv.drawContours(blank, contours, -1, (0,0,255), 1)
cv.imshow('Contours Drawn', blank)

cv.waitKey(0)