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
    biggestArea = 0
    bigRect = []
    for rectangle in boundRect:
        area = abs((rectangle[0]-rectangle[2]) * (rectangle[1]- rectangle[3]))
        x,y,w,h = rectangle
        centreX = x + (w / 2)
        if (area > biggestArea and x > 200): #magic number TODO
            biggestArea = area
            bigRect = rectangle



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

    return bigRect

def chooseTapeToFollowObstacle(left, right, boundingRect):
    #print("Bounding", boundingRect)
    if len(boundingRect) > 0:
        x,y,w,h = boundingRect
        centreX = x + (w / 2)
        centreY = y + (h / 2)
        #Check x[2]
         
        
        leftdist = safeDistance
        rightdist = safeDistance
      
        if (len(left) > 0):
           # print("left", left)
            innerLeft = left[0][0]
            
            #Find the intercept of the horizontal line from the bounding box centre to the laneline
            
            mleft = (  innerLeft[3] - innerLeft[1] /innerLeft[2] -innerLeft[0])
            leftIntercept = (centreX - innerLeft[3])/mleft + innerLeft[2]

            leftdist = abs(centreX - leftIntercept)

        if (len(right) > 0):
            # print("right", right)
            # print("rightin", right[0])
            #Find the intercept of the horizontal line from the bounding box centre to the laneline
            innerRight = right[0][0]
            mright = (innerRight[3] - innerRight[1] / innerRight[2] - innerRight[0])
            rightIntercept = (centreX - innerRight[3])/mright + innerRight[2]

            rightdist = abs(centreX - rightIntercept)
        else:
            print("yo")

        if (leftdist > rightdist):
            print("Go left side", leftdist, rightdist)
            return [True, leftdist,]
        else:
            print("Go right side", leftdist, rightdist)
            return [False, rightdist]    

    print("No bounding")
#Target Process:
#Centre of obstacle.
#start a tracking process.
#If < m pixels from yellow, go blue side (get gradient and do intercept with y)
#  

