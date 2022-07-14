import cv2 as cv
import numpy as np
import random

random.seed(12345)
minArea = 500
safeDistance = 200


def getPurpleBoundingBox(thresholded, undistorted):
    allContours, _ = cv.findContours(thresholded, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = []
    for i, contour in enumerate(allContours):
        contourArea = cv.contourArea(contour)
        # print("ContourArea", contourArea)
        if contourArea < minArea:
            continue
        contours.append(contour)

    # Approximate contours to polygons + get bounding rects and circles
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    # centers = [None]*len(contours)
    # radius = [None]*len(contours)
    

    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, 3, True)
        boundRect[i] = cv.boundingRect(contours_poly[i])
        # centers[i], radius[i] = cv.minEnclosingCircle(contours_poly[i])
    area = 0
    for rectangle in boundRect:
        area = abs((rectangle[0]-rectangle[2]) * (rectangle[1]- rectangle[3]))

    drawing = np.zeros((undistorted.shape[0], undistorted.shape[1], 3), dtype=np.uint8)
    # Draw polygonal contour + bonding rects + circles
    for i in range(len(contours)):
        color = (0, 255, 0)
        cv.drawContours(drawing, contours_poly, i, color)
        cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
 (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
        # cv.circle(drawing, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), color, 2)
    
    # print("Bound rect", boundRect)

    # Show in a window
    cv.imshow('Contours', drawing)
    ##TODO do AREA CHECK and output the biggest one only.

    return boundRect

def chooseTapeToFollowObstacle(left, right, boundingRect):
    print("Bounding", boundingRect)
    if len(boundingRect) > 0:
        x,y,w,h = boundingRect
        centreX = x + (w / 2)
        centreY = y + (h / 2)
        #Check x[2]

        
        leftdist = safeDistance
        rightdist = safeDistance

        if len(left > 0):
            #Find the intercept of the horizontal line from the bounding box centre to the laneline
            mleft = (left[3] - left[1] / left[2] - left[0])
            leftIntercept = (centreX - left[3])/mleft + left[2]

            xdist = abs(centreX - leftIntercept)

        if len(right > 0):
            #Find the intercept of the horizontal line from the bounding box centre to the laneline
            mright = (right[3] - right[1] / right[2] - right[0])
            rightIntercept = (centreX - right[3])/mright + right[2]

            ydist = abs(centreX - rightIntercept)

        if (xdist > ydist):
            print("Go x side", xdist)
            return [True, xdist]
        else:
            print("Go y side", ydist)
            return [False, ydist]    

    print("No bounding")
#Target Process:
#Centre of obstacle.
#start a tracking process.
#If < m pixels from yellow, go blue side (get gradient and do intercept with y)
#  

