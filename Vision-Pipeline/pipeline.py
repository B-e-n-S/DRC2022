from doctest import testsource
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
import constants
from VideoGet import VideoGet
import PurpleBox

blueisLeft = True


def singlePipeline(frame):
    #Pipeline Process:
        undistorted = cameracorrection.undistort(frame)
        thresholdedYellow = imageprocessing.thresholdImage(cropped, YELLOW_LH, YELLOW_LS, YELLOW_LV, YELLOW_HH, YELLOW_HS, YELLOW_HV)
        thresholdedBlue = imageprocessing.thresholdImage(cropped, BLUE_LH, BLUE_LS, BLUE_LV, BLUE_HH, BLUE_HS, BLUE_HV)
        cv.imshow("ThresholdedYellow", thresholdedYellow)
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
        #print("laneLines", laneLines)

        #Display Lines
        laneLinesImage = lanedetection.display_lines(undistorted, laneLines)
        cv.imshow("lane lines", laneLinesImage)

def individualLaneDetection(frame, original, isLeft):
        open = imageprocessing.openImage(frame)
        # edges = cv.Canny(frame, 200, 400)
        test = cv.Canny(open, 200, 400)
        # cv.imshow("Canny", edges)
        # cv.imshow("Open", test)
   
        #Detect lane section
        lineSegments = lanedetection.detectLineSegments(test)
        #cv.imshow("bruh", lanedetection.display_lines(original, lineSegments))
        laneLine = lanedetection.singlelineDetect(frame, lineSegments, isLeft)
        #display = lanedetection.display_lines(original, laneLine)
        # cv.imshow("Go bro", display)

        return laneLine

##TODO: Check if this offset is from the top and problematic 
# The lfe       
def getTargetPoint(lines, width, height):
    _, _, left_x2, _ = lines[0][0]
    _, _, right_x2, _ = lines[1][0]
    mid = int(width / 2)
    x_offset = int((left_x2 + right_x2) / 2 - mid)
    y_offset = int(height / cropamount)
    return [x_offset, y_offset]

def getTargetPointLeft(left, width, height):
    left_x2 = left[0][0][2] 
    mid = int(width / 2)
    x_offset = int(left_x2 + singleLineOffset - mid)
    y_offset = int(height / cropamount)
    return [x_offset, y_offset]

def getTargetPointRight(right, width, height):
   
    right_x2 = right[0][0][2] 
    mid = int(width / 2)
    x_offset = int(right_x2 - singleLineOffset - mid)
    y_offset = int(height / cropamount)
    return [x_offset, y_offset]  

#Works out a target point from both lane lines and calculates a purePursuit value from this.
def separatedPipeline(frame): 
    undistorted = cameracorrection.undistort(frame)
    cropped = imageprocessing.region_of_interestMask(undistorted)
    cv.imshow("cropped", cropped)
    thresholdedYellow = imageprocessing.thresholdImage(cropped, YELLOW_LH, YELLOW_LS, YELLOW_LV, YELLOW_HH, YELLOW_HS, YELLOW_HV)
    thresholdedBlue = imageprocessing.thresholdImage(cropped, BLUE_LH, BLUE_LS, BLUE_LV, BLUE_HH, BLUE_HS, BLUE_HV)
    cv.imshow("ThresholdedYellow", thresholdedYellow)
    yellow = individualLaneDetection(thresholdedYellow, undistorted, True)
    # print("yellow", yellow)
    width = undistorted.shape[1]
    height =  undistorted.shape[0]
    blue = individualLaneDetection(thresholdedBlue, undistorted, False)
    
    left = yellow #Adjust assignment here if this is differen
    right = blue
    # print("left", left)
    # print("right", right)
    combined = left + right
    targetPoint = [0, 0]
    ##Fix this logic
    print(len(left), len(right))
    if (len(left) > 0 and len(right) > 0):
       # print("actually doing")
        targetPoint = getTargetPoint(combined, width, height)
    
    elif (len(left)> 0):
      #  print("doing lef")
        targetPoint = getTargetPointLeft(left, width, height)

    elif (len(right) > 0):
      #  print("doing right")
        targetPoint = getTargetPointRight(right, width, height)
      #  print("targetPoint", targetPoint)

    laneLinesImage = lanedetection.display_lines(undistorted, combined)
    delta = purepursuit.purePursuitController(targetPoint)
    deltaDegrees = math.degrees(delta)
    #Stabilise delta value:
    stabilisedDelta = np.clip(delta, constants.prevDelta-8, constants.prevDelta+8 )
    croppedLess = imageprocessing.region_of_interestMaskLESS(undistorted)
    thresholdPurple = imageprocessing.thresholdImage(croppedLess,  PURPLE_LH, PURPLE_LS, PURPLE_LV, PURPLE_HH, PURPLE_HS, PURPLE_HV)
    purpleBox = PurpleBox.getPurpleBoundingBox(thresholdPurple, undistorted)
    PurpleBox.chooseTapeToFollowObstacle(left, right, purpleBox)

    cv.line(laneLinesImage, (int(width//2), int(height)), (int(targetPoint[0] + width/2), int(targetPoint[1])), (0, 0, 255), thickness = 3)
    cv.imshow("LaneLines", laneLinesImage) 



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
    dir = "C:/Users/b3nsc/OneDrive - The University of Sydney (Students)/Documents/University/Societies/Robotics/DRC Code/AlternatingPurple.avi"

    # videoGetter = VideoGet(dir).start()

    
    video = cv.VideoCapture(dir)
    if(video.isOpened() == False):
        print("Error reading file")

    create_global_variables()

    while (True):
        ret, frame = video.read()
        # frame = videoGetter.frame
        # if ret == True:
            #singlePipeline(frame)
        separatedPipeline(frame)
            
            

        k = cv.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            
            break
        # else:
        #     break
    # videoGetter.stop()
    # video.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    print("Initialising...")
    print(cv.__version__)
    main()

