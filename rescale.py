import cv2 as cv

#Preferred rescale method for live video
def changeRes(width, height):
    capture.set(3, width)
    capture.set(4, height) 

#Works for live video, files or non-live.
def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

#capture = cv.VideoCapture('Images/doglog.mp4') #integer arguments for webcam 0 webcam, 1 is 2nd usb camera etc.
capture = cv.VideoCapture(1)  #Get from webcam probably change to 1 for - video 


changeRes(1080, 720)
##Display each frame one at a time

while True:
    isTrue, frame = capture.read()
    
   
    #frame_resized = rescaleFrame(frame, scale=.2)
    
    cv.imshow('Video', frame)
    #cv.imshow("Video Resized", frame_resized)
    ##Get out of loop. May make more sense to use a flag.
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
capture.release()
cv.destroyAllWindows()