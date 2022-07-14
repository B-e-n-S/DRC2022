from cgi import test


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

cropamount = 3 #consider 2 thirds of screen

speed = 92
singleLineOffset = 150
maximumAngleChange = 15 #TODO: See if remove

#Global non-constant variables
def create_global_variables():
    global prevDelta# must declare it to be a global first
    # modifications are thus reflected on the module's global scope
    prevDelta = 0

