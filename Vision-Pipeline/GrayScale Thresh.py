from __future__ import print_function
import cv2 as cv
import argparse
import cameracorrection
import imageprocessing

max_value = 255
low_I = 34
high_I = 46
high_S = 255
high_V = 255
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_I_name = 'Low I'
high_I_name = 'High I'

def on_low_I_thresh_trackbar(val):
    global low_I
    global high_I
    low_I = val
    low_I = min(high_I-1, low_I)
    cv.setTrackbarPos(low_I_name, window_detection_name, low_I)
def on_high_I_thresh_trackbar(val):
    global low_I
    global high_I
    high_I = val
    high_I = max(high_I, low_I+1)
    cv.setTrackbarPos(high_I_name, window_detection_name, high_I)
#Works for live video, files or non-live.
def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera divide number.', default=0, type=int)
args = parser.parse_args()
#cap = cv.VideoCapture(args.camera)
cap = cv.VideoCapture(1)
#cap = cv.VideoCapture('Images/CorrectTape.mp4')
cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name)
cv.createTrackbar(low_I_name, window_detection_name , low_I, max_value, on_low_I_thresh_trackbar)
cv.createTrackbar(high_I_name, window_detection_name , high_I, max_value, on_high_I_thresh_trackbar)

while True:
    
    ret, frameundistort = cap.read()
    if frameundistort is None:
        break
    #frame = rescaleFrame(frame, 0.4)
    frame = cameracorrection.undistort(frameundistort)
  
  
    frame_GRAY = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('gray', frame_GRAY)
    frame_threshold = cv.inRange(frame_GRAY, (low_I), (high_I))
    cv.imshow(window_capture_name, frame)
    frame_opened = imageprocessing.openImage(frame_threshold)
    cv.imshow('opened', frame_opened)
    cv.imshow(window_detection_name, frame_threshold)
    
    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break