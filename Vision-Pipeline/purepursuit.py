import numpy as np
import math

distanceToHorizontalPoint = 0.4 # the 167pixels matches wih this value in metres
lengthBetweenAxles = 0.36 #Change to measured value in meteres
metersPerPixelHorizontalAtTargetPoint = 0.002 #Num meters per pixel along the x axis at the target point. Todo measure
ylength = distanceToHorizontalPoint + lengthBetweenAxles

#Forumla: Basially need to use back axle. So for fixed angle know distance to front axle. 
#Know distance to pixel conversion on floor.
#Hence can calculate the angle.

def purePursuitController(targetPoint):
    if (targetPoint[1] != 159): 
        print ("Cropping of vision must have changed. Need to remeasure")
    offsetMetres =  targetPoint[0] * metersPerPixelHorizontalAtTargetPoint
    alpha = math.atan(offsetMetres / ylength)
    print("alpha", alpha)
    delta = np.arctan(2 * lengthBetweenAxles * math.sin(alpha)/ distanceToHorizontalPoint)
    return delta
