import cv2 as cv
import numpy as np

#Works for live video, files or non-live.
def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


##Height, width, num of colour channels.
blank = np.zeros((500, 500, 3), dtype='uint8')
#cv.imshow('Blank', blank)
img = cv.imread('Images/cat.jpg')
imgScaled = rescaleFrame(img, scale=0.4)

#cv.imshow('Cat', imgScaled)


#1. Paint the image a certain colour
blank[200:300, 300:400] = 0,0, 255
#cv.imshow('Red', blank)

#2. Draw a Rectangle.
#cv.rectangle(blank, (0,0), (250, 500), (0, 255, 0), thickness=cv.FILLED)
cv.rectangle(blank, (50,0), (blank.shape[1]//2, blank.shape[0]//2), (0, 255, 0), thickness=2)  
#cv.imshow('Green', blank)

#3. Draw a circle
cv.circle(blank, (blank.shape[1]//2, blank.shape[0]//2), 40, (0, 0, 255), thickness = -1)
#cv.imshow('Circle', blank)

#4. Draw a line
cv.line(blank, (100,250), (blank.shape[1]//2 , blank.shape[0]//2+100), (255, 255, 255), thickness = 3)


#5. Write text
cv.putText(blank, 'Line Detected', (250, 100), cv.FONT_HERSHEY_TRIPLEX, 1.0, (250, 0, 0), 2) 
cv.imshow('Text', blank)

cv.waitKey(0)