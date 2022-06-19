import cv2 as cv

# img = cv.imread('Images/Cat.jpg')

# cv.imshow('Cat', img)

# cv.waitKey(0) ##Keyboard binding function for key to be pressed. 

#Reading video
capture = cv.VideoCapture('Images/doglog.mp4') #integer arguments for webcam 0 webcam, 1 is 2nd usb camera etc.
#capture = cv.VideoCapture(1)  #Get from webcam probably change to 1 for - video 

def rescaleFrame(frame, scale=0.75):
    width = frame.shape[1] * scale
    height = frame.shape[0] * scale

##Display each frame one at a time
while True:
    isTrue, frame = capture.read()
    
    

    cv.imshow('Video', frame)

    ##Get out of loop. May make more sense to use a flag.
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
capture.release()
cv.destroyAllWindows()