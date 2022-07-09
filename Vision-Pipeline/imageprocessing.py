import cv2 as cv
import numpy as np

#Some methods adapted from https://towardsdatascience.com/deeppicar-part-4-lane-following-via-opencv-737dd9e47c96

kernel = cv.getStructuringElement(cv.MORPH_RECT, (3,3))

#Thresholds based on HSV range
def thresholdImage(frameBGR, lowH, lowS, lowV, highH, highS, highV) :
    frame_HSV = cv.cvtColor(frameBGR, cv.COLOR_BGR2HSV)
    return cv.inRange(frame_HSV, (lowH, lowS, lowV), (highH, highS, highV))

#Removes noise from image
def openImage(frame):
    return cv.morphologyEx(frame, cv.MORPH_OPEN, kernel)

#Crops image to only consider bottom half of screen
def region_of_interest(edges):
    height, width = edges.shape
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

