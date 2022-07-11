import numpy as np
import math

lookaheadDistance = 0.4
lengthBetweenAxles = 0.3

def purePursuitController(targetPoint, lookAheadDistance):
    alpha = math.atan(targetPoint[0] / targetPoint[1])
    delta = np.arctan(2 * lengthBetweenAxles * math.sin(alpha)/ lookAheadDistance)
    return delta