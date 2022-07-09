import cv2 as cv

video = cv.VideoCapture(1)
if(video.isOpened() == False):
    print("Error reading file")

frame_width = int(video.get(3))
frame_height = int(video.get(4))

size = (frame_width, frame_height)

result = cv.VideoWriter('Testfootage.avi', cv.VideoWriter_fourcc(*'MJPG'), 30, size)

while (True):
    ret, frame = video.read()

    if ret == True:
        #Write the frme
        result.write(frame)
        cv.imshow('Frame', frame)

        #Press esc to stop process
        k = cv.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break

    else:
        break
video.release()
result.release()

cv.destroyAllWindows()

print("Video successfully saved")