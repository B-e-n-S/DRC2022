from turtle import end_fill
import cv2 as cv
from cv2 import threshold
from cv2 import bitwise_and
from cv2 import bitwise_or
from cv2 import undistortPointsIter
from matplotlib import lines
import math
import numpy as np
import time
#from CountsPerSec import CountsPerSec
from threading import Thread

#ConstantsFile
YELLOW_LH = 25 #25
YELLOW_LS = 40 #45
YELLOW_LV = 181 #100
YELLOW_HH = 35 #35
YELLOW_HS = 244 #181
YELLOW_HV = 255 #255


BLUE_LH = 103 #70
BLUE_LS = 70 #26
BLUE_LV = 50 #50
BLUE_HH = 110 #110
BLUE_HS = 250 #198 
BLUE_HV = 255 #255

GREEN_LH = 34 #31
GREEN_LS = 51 #31
GREEN_LV = 93 #120
GREEN_HH = 46 #40
GREEN_HS = 255 #244
GREEN_HV = 255 #255

PURPLE_LH = 125 
PURPLE_LS = 65 
PURPLE_LV = 16 
PURPLE_HH = 180 
PURPLE_HS = 255
PURPLE_HV = 206 

BLACK_LI = 0 
BLACK_HI = 85 


cropamount = 2.4 #consider 2 thirds of screen

speed = 92
singleLineOffset = 150
maximumAngleChange = 10 #TODO: See if remove
distanceToHorizontalPoint = 0.40 # the 167pixels matches wih this value in metres
lengthBetweenAxles = 0.36 #Change to measured value in meteres
metersPerPixelHorizontalAtTargetPoint = 0.002 #Num meters per pixel along the x axis at the target point. Todo measure
ylength = distanceToHorizontalPoint + lengthBetweenAxles
prevDelta = 0
RUNTIME = 1000 #RUNTIME in seconds

##TODO: Pick the wait to start checking for the green tape time
timeTillCheckForFinishLine = 5
greenCounter = 0

# prevDelta = {"prevDelta" : 25}

class VideoGet:
    """
        Class that continuously gets frames from a VideoCapture object
        with a dedicated thread.
    """
    def __init__(self, src=0):
        self.stream = cv.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True                    


#Global non-constant variables
def create_global_variables():
    meme = None
    global prevDelta# must declare it to be a global first
    # modifications are thus reflected on the module's global scope
    prevDelta = 0
    global greenCounter
    greenCounter = 0




##ImageProcessing File

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
    # cv.imshow('Blank image', blank)

    # mask = cv.circle(blank, (frame.shape[1]//2, frame.shape[0]//2), 200, 255, -1)
    #Bottom half of the image
    mask = cv.rectangle(blank, (0, int(height - height//cropamount)), (width, int(height-height//10)), 255, thickness=-1)  
    # cv.imshow('Mask', mask)

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

##Camera Correction File
"""
Hard coded distortion coefficients and values for the Raspberry Pi Wide Angle camera
"""
dist_coeffs = np.array([-3.33440903e-01,  1.22459385e-01, -1.36736921e-03,  1.50750541e-04,
                        -2.10696063e-02])
    
camera_matrix = np.array([[240.84171937,   0, 343.73323286],
                            [   0, 240.38352732, 223.76385059],
                            [  0,            0,             1         ]])

optimised_camera_matrix = np.array([[240.46542358,   0,         343.19617006],
                                    [  0,   239.88273621, 223.29768298],
                                    [  0,           0,          1           ]])
roi = (0, 0, 639, 479)

def undistort(image) -> any:
    img_undistort = cv.undistort(image, camera_matrix, dist_coeffs, None, optimised_camera_matrix)
    x, y, w, h = roi
    cv.rectangle(img_undistort, (x,y), (x+w, y+h), (0,0,255), 2)
    img_undistort = img_undistort[y:y+h, x:x+w]
    return img_undistort

##LaneDetectionFile

# Uses Hough algorithm to detect line segments. TODO: Needs tuning
# Explanation: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
def detectLineSegments(frame):
    return detectLineSegmentsDetailed(frame, 10, 5)

def detectLineSegmentsDetailed(frame, minLineLength, maxLineGap):   
    # tuning min_threshold, minLineLength, maxLineGap is a trial and error process by hand
    rho = 1 #distance precision in pixel, i.e. 1 pixel
    angle = np.pi / 180 # angular precision in radian, i.e. 1 degree
    min_threshold = 10  # minimal of votes
    line_segments = cv.HoughLinesP(frame, rho, angle, min_threshold, 
                                    np.array([]), minLineLength, maxLineGap)
    #print("Segment", line_segments)
    return line_segments



#Takes line's slope and intercept and returns endpoints of the line segment.
def make_points(frame, line):
    height = frame.shape[0]
    width = frame.shape[1]
    slope, intercept = line
    # print("slope", slope)
    y1 = height  # bottom of the frame
    y2 = int(y1 * 1 / 2)  # make points from middle of the frame down
    # print("y2", y2)
    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    # print([x1, y1, x2, y2])
    return [[x1, y1, x2, y2]]

#Takes line's slope and intercept and returns endpoints of the line segment.
def make_points2(frame, line):
    height, width, _ = frame.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]

def singlelineDetect(frame, line_segments):
    lane_lines = []
    if line_segments is None:
        print("No line_segments detected")
        return lane_lines

    height, width = frame.shape
    combinedFit = []
    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            #print("We have a line segment")
            if x1 == x2:
                #print('skipping vertical line segment (slope=inf): %s' % line_segment)
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            combinedFit.append((slope, intercept))
    fitAverage = np.average(combinedFit, axis=0)
    #print(fitAverage)
    #print(combinedFit)
    if len(combinedFit) > 0:
        lane_lines.append(make_points(frame, fitAverage))
    return lane_lines    

#This could be simplified by considering the yellow and blue components separately.
def average_slope_intercept(frame, line_segments):
    """
    This function combines line segments into one or two lane lines
    If all line slopes are < 0: then we only have detected left lane
    If all line slopes are > 0: then we only have detected right lane
    """
    lane_lines = []
    if line_segments is None:
        print('No line_segment segments detected')
        return lane_lines

    height, width, _ = frame.shape
    left_fit = []
    right_fit = []

    boundary = 1/3
    left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
    right_region_boundary = width * boundary # right lane line segment should be on right 2/3 of the screen

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            #print("We have a line segment")
            if x1 == x2:
                #print('skipping vertical line segment (slope=inf): %s' % line_segment)
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    # print("left_fit_average", left_fit_average)
    if len(left_fit) > 0:
        #print("points", make_points2(frame, left_fit_average))
        lane_lines.append(make_points2(frame, left_fit_average))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(frame, right_fit_average))
    return lane_lines  

def display_lines(frame, lines, line_color=(0, 255, 0), line_width=2):
    #print(lines)
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            print("line", line)
            for x1, y1, x2, y2 in line:
                cv.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    line_image = cv.addWeighted(frame, 0.8, line_image, 1, 1)
    return line_image



def individualLaneDetection(frame, original):
        open = openImage(frame)
        # edges = cv.Canny(frame, 200, 400)
        test = cv.Canny(open, 200, 400)
        # cv.imshow("Canny", edges)
        # cv.imshow("Open", test)
   
        #Detect lane section
        lineSegments = detectLineSegments(test)
        #cv.imshow("bruh", lanedetection.display_lines(original, lineSegments))
        laneLine = singlelineDetect(frame, lineSegments)
        #display = lanedetection.display_lines(original, laneLine)
        # cv.imshow("Go bro", display)

        return laneLine

def individualLaneDetectionGreen(frame, original, minLineLength, maxLineGap):
        open = openImage(frame)
        # edges = cv.Canny(frame, 200, 400)
        test = cv.Canny(open, 200, 400)
        # cv.imshow("Canny", edges)
        # cv.imshow("Open", test)
   
        #Detect lane section
        lineSegments = detectLineSegmentsDetailed(frame, minLineLength, maxLineGap)
        #cv.imshow("bruh", lanedetection.display_lines(original, lineSegments))
        laneLine = singlelineDetect(frame, lineSegments)
        display = display_lines(original, laneLine)
        cv.imshow("Go bro", display)

        return laneLine

##TODO: Check if this offset is from the top and problematic 
# The lfe       
def getTargetPoint(lines, width, height):
    _, _, left_x2, _ = lines[0][0]
    _, _, right_x2, _ = lines[1][0]
    mid = int(width / 2)
    x_offset = int((left_x2 + right_x2) / 2 - mid)
    y_offset = int(height - height / cropamount)
    return [x_offset, y_offset]

def getTargetPointLeft(left, width, height):
    left_x2 = left[0][0][2] 
    mid = int(width / 2)
    x_offset = int(left_x2 + singleLineOffset - mid)
    y_offset = int(height - height / cropamount)
    return [x_offset, y_offset]

def getTargetPointRight(right, width, height):
    right_x2 = right[0][0][2] 
    mid = int(width / 2)
    x_offset = int(right_x2 - singleLineOffset - mid)
    y_offset = int(height - height / cropamount)
    return [x_offset, y_offset]  

##PURE-PURSUIT FILE:


#Forumla: Basially need to use back axle. So for fixed angle know distance to front axle. 
#Know distance to pixel conversion on floor.
#Hence can calculate the angle.

def purePursuitController(targetPoint):
    print("TargetPoint1", targetPoint[1])
    if (targetPoint[1] != 167): 
        print ("Cropping of vision must have changed. Need to remeasure")
    offsetMetres =  targetPoint[0] * metersPerPixelHorizontalAtTargetPoint
    alpha = math.atan(offsetMetres / ylength)
    #print("alpha", alpha)
    delta = np.arctan(2 * lengthBetweenAxles * math.sin(alpha)/ distanceToHorizontalPoint)
    return delta

##Green Figure out what to do
#Ignore the green line for the first 20 seconds 

#Return true for green
def greenCheck(undistorted):
    global greenCounter
    thresholdedGreen = thresholdImage(undistorted, GREEN_LH, GREEN_LS, GREEN_LV, GREEN_HH, GREEN_HS, GREEN_HV)
    green = individualLaneDetectionGreen(thresholdedGreen, undistorted, 40, 4)
    if (len(green) > 0):
        greenCounter = greenCounter + 1
    else:
        greenCounter = 0



    ##TODO finish


#Works out a target point from both lane lines and calculates a purePursuit value from this.
def separatedPipeline(undistorted): 
    global prevDelta
    
    cropped = region_of_interestMask(undistorted)
    cv.imshow("cropped", cropped)
    thresholdedYellow = thresholdImage(cropped, YELLOW_LH, YELLOW_LS, YELLOW_LV, YELLOW_HH, YELLOW_HS, YELLOW_HV)
    thresholdedBlue = thresholdImage(cropped, BLUE_LH, BLUE_LS, BLUE_LV, BLUE_HH, BLUE_HS, BLUE_HV)

    
  
    yellow = individualLaneDetection(thresholdedYellow, undistorted)
    # print("yellow", yellow)
    width = undistorted.shape[1]
    height =  undistorted.shape[0]
    blue = individualLaneDetection(thresholdedBlue, undistorted)
    
    
    left = yellow #Adjust assignment here if this is differen
    right = blue
    combined = left + right
    targetPoint = [0, 0]
    ##Fix this logic
    if (len(left) > 0 and len(right) > 0):
        targetPoint = getTargetPoint(combined, width, height)
    
    elif (len(left)> 0):
        targetPoint = getTargetPointLeft(left, width, height)

    elif (len(right) > 0):
        targetPoint = getTargetPointRight(right, width, height)

    laneLinesImage = display_lines(undistorted, combined)
    delta = purePursuitController(targetPoint)
    deltaDegrees = math.degrees(delta)
    #Stabilise delta value:
    print("prevDelta", prevDelta)
    stabilisedDelta = np.clip(deltaDegrees, prevDelta - maximumAngleChange, prevDelta + maximumAngleChange)
    print("prevDelta", prevDelta)
    prevDelta = stabilisedDelta
    print("prevDelta updated", prevDelta)

    cv.line(laneLinesImage, (int(width//2), int(height)), (int(targetPoint[0] + width/2), int(targetPoint[1])), (0, 0, 255), thickness = 3)
    cv.imshow("LaneLines", laneLinesImage) 
    return (speed, stabilisedDelta)



def main():
    create_global_variables()

    videoGetter = VideoGet(1).start()
    
    # video = cv.VideoCapture(1)
    # if(video.isOpened() == False):
    #     print("Error reading file")
    startTime = time.time()

    while (True):
        beginLoop = time.time()
        frame = videoGetter.frame
        undistorted = undistort(frame)
        # ret, frame = video.read()
        #singlePipeline(frame)
        speed, angle = separatedPipeline(undistorted)
        print("angle", angle)
        
        #Check the finish line after certain:
        if(time.time() - startTime > timeTillCheckForFinishLine):
            print("Go for Green")
            greenCheck(undistorted)
           


        if (time.time() - startTime > RUNTIME):
            print("Time Expired")
            break

        k = cv.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        
        loopTime = time.time() - beginLoop
        print("loopTime", loopTime)
        


    ##SET THE SPEED TO 0 at the end
    speed = 0
    
    videoGetter.stop()
    cv.destroyAllWindows()

if __name__ == "__main__":
    print("Initialising...")
    main()

