from cgi import test


yellow_LH = 25
yellow_LS = 45
yellow_LV = 100 #97
yellow_HH = 35
yellow_HS = 244
yellow_HV = 255

blue_LS = 26
blue_LV = 50
blue_LH = 70
blue_HH = 110
blue_HS = 198
blue_HV = 255

cropamount = 3 #consider 2 thirds of screen

speed = 92
singleLineOffset = 150
maximumAngleChange = 15 #TODO: See if remove

#Global non-constant variables
def create_global_variables():
    global prevDelta# must declare it to be a global first
    # modifications are thus reflected on the module's global scope
    prevDelta = 0

