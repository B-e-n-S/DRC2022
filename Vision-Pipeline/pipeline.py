import cv2 as cv
from cv2 import threshold
from cv2 import bitwise_and
from cv2 import bitwise_or
from cv2 import undistortPointsIter
from matplotlib import lines
import imageprocessing
import cameracorrection
import lanedetection
import math
import numpy as np
import purepursuit
from constants import *

blueisLeft = True


def singlePipeline(frame):
    #Pipeline Process:
        undistorted = cameracorrection.undistort(frame)
        thresholdedYellow = imageprocessing.thresholdImage(undistorted, yellow_LH, yellow_LS, yellow_LV, yellow_HH, yellow_HS, yellow_HV)
        cv.imshow("ThresholdedYellow", thresholdedYellow)
        thresholdedBlue = imageprocessing.thresholdImage(undistorted, blue_LH, blue_LS, blue_LV, blue_HH, blue_HS, blue_HV)
        thresholded = bitwise_or(thresholdedYellow, thresholdedBlue)
     
        #opened = imageprocessing.openImage(thresholded) Doesn't seem to help
        cv.imshow("Thresholded", thresholded)
        #cv.imshow("open", opened)
        edges = cv.Canny(thresholded, 200, 400)
        cv.imshow("Canny", edges)
        cropped = imageprocessing.region_of_interest(edges)
        cv.imshow("Cropped", cropped)

        #Detect lane section
        lineSegments = lanedetection.detectLineSegments(cropped)
        #print("lineSegments2", lineSegments)
        laneLines = lanedetection.average_slope_intercept(frame, lineSegments)
        print("laneLines", laneLines)

        #Display Lines
        laneLinesImage = lanedetection.display_lines(undistorted, laneLines)
        cv.imshow("lane lines", laneLinesImage)

def individualLaneDetection(frame, original):
        open = imageprocessing.openImage(frame)
        # edges = cv.Canny(frame, 200, 400)
        test = cv.Canny(open, 200, 400)
        # cv.imshow("Canny", edges)
        # cv.imshow("Open", test)
   
        #Detect lane section
        lineSegments = lanedetection.detectLineSegments(test)
        #cv.imshow("bruh", lanedetection.display_lines(original, lineSegments))
        laneLine = lanedetection.singlelineDetect(frame, lineSegments)
        #display = lanedetection.display_lines(original, laneLine)
        # cv.imshow("Go bro", display)

        return laneLine

##TODO: Check if this offset is from the top and problematic        
def getTargetPoint(lines, width, height):
    _, _, left_x2, _ = lines[0][0]
    _, _, right_x2, _ = lines[1][0]
    mid = int(width / 2)
    x_offset = int((left_x2 + right_x2) / 2 - mid)
    y_offset = int(height - height / cropamount)
    return [x_offset, y_offset]

def getTargetPointLeft(left, width, height):
    left_x2 = left[2] 
    mid = int(width / 2)
    x_offset = int(left_x2 + singleLineOffset - mid)
    y_offset = int(height - height / cropamount)
    return [x_offset, y_offset]

def getTargetPointRight(right, width, height):
    right_x2 = right[2] 
    mid = int(width / 2)
    x_offset = int(right_x2 - singleLineOffset - mid)
    y_offset = int(height - height / cropamount)
    return [x_offset, y_offset]

def convertToDrive(targetPoint, combined, undistorted, width, height):
    laneLinesImage = lanedetection.display_lines(undistorted, combined)
    delta = purepursuit.purePursuitController(targetPoint)
    deltaDegrees = math.degrees(delta)
    #Stabilise delta value:
    stabilisedDelta = np.clip(delta, prevDelta-8, prevDelta+8 )
    
    cv.line(laneLinesImage, (int(width//2), int(height)), (int(targetPoint[0] + width/2), int(targetPoint[1])), (0, 0, 255), thickness = 3)
    cv.imshow("LaneLines", laneLinesImage)
    return (speed, delta)
  

#Works out a target point from both lane lines and calculates a purePursuit value from this.
def bothLaneMode(undistorted, left, right, width, height):
    combined = left + right
    # print("combined", combined)
    targetPoint = None
    if (len(combined) > 1):
        targetPoint = getTargetPoint(combined, width, height)
    if (targetPoint is not None):
        convertToDrive(targetPoint, combined, undistorted, width, height)        
    return (None, None)

def leftLaneOnly(undistorted, left, width, height):
    targetPoint = getTargetPointLeft(left,width, height)
    convertToDrive(targetPoint, left, undistorted, width, height) #Will break things

def separatedPipeline(frame): 
    undistorted = cameracorrection.undistort(frame)
    cropped = imageprocessing.region_of_interestMask(undistorted)
    cv.imshow("cropped", cropped)
    thresholdedYellow = imageprocessing.thresholdImage(cropped, yellow_LH, yellow_LS, yellow_LV, yellow_HH, yellow_HS, yellow_HV)
    thresholdedBlue = imageprocessing.thresholdImage(cropped, blue_LH, blue_LS, blue_LV, blue_HH, blue_HS, blue_HV)
    cv.imshow("ThresholdedYellow", thresholdedYellow)
    yellow = individualLaneDetection(thresholdedYellow, undistorted)
    # print("yellow", yellow)
    width = undistorted.shape[1]
    height =  undistorted.shape[0]
    blue = individualLaneDetection(thresholdedBlue, undistorted)
    
    left = blue #Adjust assignment here if this is differen
    right = yellow
    
    if (len(left) > 0 & len(right) > 0):
        return bothLaneMode(undistorted, left, right,width, height)
    
    else if (len(left)> 0):
        return leftLaneOnly(undistorted, left, width, height)
    
    else:
        return (0, 0)

   #Check if there is a blue and yellow line -> do normal algorithm
   #Else, check if there is just a blue lane -> run logic on blue.
   #Else, check if there is a yellow lane -> run logic on yellow.
   #Else run lost robot problem.
   
    # # print("blue", blue)
    # combined = blue + yellow
    # # print("combined", combined)
    # targetPoint = None
    # if (len(combined) > 1):
    #     targetPoint = getTargetPoint(combined, width, height)
      
    


    # print(width, height)

    # print("targetPoint", targetPoint)

 

    # #yellow.append(blue)
    # #print(combined)
    # print()
    # laneLinesImage = lanedetection.display_lines(undistorted, combined)
    # if targetPoint is not None:
    #     delta = purepursuit.purePursuitController(targetPoint)
    #     print("Delta", delta)
    #     cv.line(laneLinesImage, (int(width//2), int(height)), (int(targetPoint[0] + width/2), int(targetPoint[1])), (0, 0, 255), thickness = 3)
   
    # #cv.line(laneLinesImage, (100, 0), (int(targetPoint[0]), int(targetPoint[1])), (0, 0, 255), thickness = 3)
    # cv.imshow("lane lines", laneLinesImage)





def main():
    video = cv.VideoCapture(1)
    if(video.isOpened() == False):
        print("Error reading file")

    while (True):
        ret, frame = video.read()

        if ret == True:
            #singlePipeline(frame)
            separatedPipeline(frame)
            
            

            k = cv.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break

        else:
            break

    video.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    print("Initialising...")
    main()

