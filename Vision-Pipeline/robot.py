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
import purepursuit
import pipeline
import constants

def main():
    constants.create_global_variables
    video = cv.VideoCapture(1)
    if(video.isOpened() == False):
        print("Error reading file")

    while (True):
        ret, frame = video.read()

        if ret == True:
            #singlePipeline(frame)
            speed, angle = pipeline.separatedPipeline(frame)
            
            

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

