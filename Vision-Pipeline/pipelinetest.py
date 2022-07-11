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
from constants import *

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
        
def getTargetPoint(lines, width, height):
    _, _, left_x2, _ = lines[0][0]
    _, _, right_x2, _ = lines[1][0]
    mid = int(width / 2)
    x_offset = (left_x2 + right_x2) / 2 - mid
    y_offset = int(height / cropamount)
    return (x_offset, y_offset)


def separatedPipeline(frame):
    undistorted = cameracorrection.undistort(frame)
    cropped = imageprocessing.region_of_interestMask(undistorted)
    cv.imshow("cropped", cropped)
    thresholdedYellow = imageprocessing.thresholdImage(cropped, yellow_LH, yellow_LS, yellow_LV, yellow_HH, yellow_HS, yellow_HV)
    thresholdedBlue = imageprocessing.thresholdImage(cropped, blue_LH, blue_LS, blue_LV, blue_HH, blue_HS, blue_HV)
    cv.imshow("ThresholdedYellow", thresholdedYellow)
    yellow = individualLaneDetection(thresholdedYellow, undistorted)
    print("yellow", yellow)

    blue = individualLaneDetection(thresholdedBlue, undistorted)
    print("blue", blue)
    combined = blue + yellow
    print("combined", combined)
    if (len(combined) > 1):
        targetPoint = getTargetPoint(combined, undistorted.shape[1], undistorted.shape[0])
        # print(targetPoint)




    #yellow.append(blue)
    #print(combined)
    laneLinesImage = lanedetection.display_lines(undistorted, combined)
    cv.imshow("lane lines", laneLinesImage)



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

