import cv2 as cv
from cv2 import threshold
from cv2 import bitwise_and
from cv2 import bitwise_or
from matplotlib import lines
import imageprocessing
import cameracorrection
import lanedetection
from constants import *

video = cv.VideoCapture(1)
if(video.isOpened() == False):
    print("Error reading file")

while (True):
    ret, frame = video.read()

    if ret == True:

        #Pipeline Process:
        undistorted = cameracorrection.undistort(frame)
        thresholdedYellow = imageprocessing.thresholdImage(undistorted, yellow_LH, yellow_LS, yellow_LV, yellow_HH, yellow_HS, yellow_HV)
        cv.imshow("ThresholdedYellow", thresholdedYellow)
        thresholdedBlue = imageprocessing.thresholdImage(undistorted, blue_LH, blue_LS, blue_LV, blue_HH, blue_HS, blue_HV)
        thresholded = bitwise_or(thresholdedYellow, thresholdedBlue)
     
        opened = imageprocessing.openImage(thresholded)
        cv.imshow("Thresholded", thresholded)
        cv.imshow("open", opened)
        edges = cv.Canny(opened, 200, 400)
        cv.imshow("Canny", edges)
        cropped = imageprocessing.region_of_interest(edges)
        cv.imshow("Cropped", cropped)

        #Detect lane section
        lineSegments = lanedetection.detectLineSegments(cropped)
        #print("lineSegments2", lineSegments)
        laneLines = lanedetection.average_slope_intercept(frame, lineSegments)
        print("laneLines", laneLines)

        #Display Lines
        laneLinesImage = lanedetection.display_lines(undistorted, lineSegments)
        cv.imshow("lane lines", laneLinesImage)


        k = cv.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break

    else:
        break

video.release()
cv.destroyAllWindows()

cv.destroyAllWindows()

