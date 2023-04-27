import cv2 as cv
import numpy as np
# Uses Hough algorithm to detect line segments. TODO: Needs tuning
# Explanation: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
def detectLineSegments(frame):
    # tuning min_threshold, minLineLength, maxLineGap is a trial and error process by hand
    rho = 1 #distance precision in pixel, i.e. 1 pixel
    angle = np.pi / 180 # angular precision in radian, i.e. 1 degree
    min_threshold = 10  # minimal of votes
    line_segments = cv.HoughLinesP(frame, rho, angle, min_threshold, 
                                    np.array([]), minLineLength=10, maxLineGap=5)
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

def singlelineDetect(frame, line_segments, isLeft):
  
    lane_lines = []
    if line_segments is None:
        print("No line_segments detected")
        return lane_lines

    height, width = frame.shape
    boundary = 1/3
    left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
    right_region_boundary = width * boundary
    combinedFit = []
    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            #print("We have a line segment")
            if x1 == x2:
                #print('skipping vertical line segment (slope=inf): %s' % line_segment)
                continue
            if (isLeft and (x1 > left_region_boundary or x2 >left_region_boundary)):
                print("Skip left")
                continue
            elif(isLeft != True and (x1 < right_region_boundary or x2 < right_region_boundary)):
                print("Skip right")
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

