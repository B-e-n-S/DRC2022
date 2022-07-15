import cv2 as cv
import numpy as np
import constants

#Some methods adapted from https://towardsdatascience.com/deeppicar-part-4-lane-following-via-opencv-737dd9e47c96

kernel = cv.getStructuringElement(cv.MORPH_RECT, (3,3))

#Thresholds based on HSV range
def thresholdImage(frameBGR, lowH, lowS, lowV, highH, highS, highV) :
    frame_HSV = cv.cvtColor(frameBGR, cv.COLOR_BGR2HSV)
    return cv.inRange(frame_HSV, (lowH, lowS, lowV), (highH, highS, highV))

#Removes noise from image
def openImage(frame):
    return cv.morphologyEx(frame, cv.MORPH_OPEN, kernel)

def region_of_interestMask(frame):
    height = frame.shape[0] 
    width = frame.shape[1]
    maskinit = np.zeros_like(frame)
     # only focus bottom half of the screen
    blank = np.zeros(frame.shape[:2], dtype='uint8')
    cv.imshow('Blank image', blank)

    # mask = cv.circle(blank, (frame.shape[1]//2, frame.shape[0]//2), 200, 255, -1)
    #Bottom half of the image
    mask = cv.rectangle(blank, (0, height - height//constants.cropamount), (width, height-height//10), 255, thickness=-1)  
    cv.imshow('Mask', mask)

    masked = cv.bitwise_and(frame, frame, mask=mask)
    #cv.imshow("Masked", masked)
    return masked

#Crops image to only consider bottom half of screen
def region_of_interest(edges):
    height = edges.shape[0] 
    width = edges.shape[1]
 
    mask = np.zeros_like(edges)

    # only focus bottom half of the screen
    polygon = np.array([[
        (0, height * 1 / 2),
        (width, height * 1 / 2),
        (width, height),
        (0, height),
    ]], np.int32)

    cv.fillPoly(mask, polygon, 255)
    cropped_edges = cv.bitwise_and(edges, mask)
    return cropped_edges

#Crops image to only consider bottom half of screen
def region_of_interestMaskLESS(frame):
    height = frame.shape[0] 
    width = frame.shape[1]
    maskinit = np.zeros_like(frame)
     # only focus bottom half of the screen
    blank = np.zeros(frame.shape[:2], dtype='uint8')
    cv.imshow('Blank image', blank)

    # mask = cv.circle(blank, (frame.shape[1]//2, frame.shape[0]//2), 200, 255, -1)
    #Bottom half of the image
    mask = cv.rectangle(blank, (0, height//3), (width, height-height//8), 255, thickness=-1)  
    cv.imshow('Mask', mask)

    masked = cv.bitwise_and(frame, frame, mask=mask)
    #cv.imshow("Masked", masked)
    return masked

    cv.fillPoly(mask, polygon, 255)
    cropped_edges = cv.bitwise_and(edges, mask)
    return cropped_edges

