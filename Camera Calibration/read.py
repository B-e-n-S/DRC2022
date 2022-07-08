import cv2 as cv

# img = cv.imread('Images/Cat.jpg')

# cv.imshow('Cat', img)

# cv.waitKey(0) ##Keyboard binding function for key to be pressed. 
# codec = 0x47504A4D # MJPG
# codec = 844715353.0 # YUY2

#Reading video
capture = cv.VideoCapture(1) #integer arguments for webcam 0 webcam, 1 is 2nd usb camera etc.
codec = 1196444237.0 # MJPG
# print 'fourcc:', decode_fourcc(codec)

capture.set(cv.CAP_PROP_FRAME_WIDTH, 640)
width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
print(width, height)
print("fps", capture.get(cv.CAP_PROP_FPS))
##Display each frame one at a time
while True:
    isTrue, frame = capture.read()
    
    

    cv.imshow('Video', frame)

    ##Get out of loop. May make more sense to use a flag.
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
capture.release()
cv.destroyAllWindows()