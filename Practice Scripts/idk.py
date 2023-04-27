
#Global non-constant variables
def create_global_variables():
    global numerator# must declare it to be a global first
    # modifications are thus reflected on the module's global scope
    numerator = 2


def increaseNumberBy(num):
    print("numerator was", numerator)
    numerator = numerator + num
    print("numerator is now", numerator)
    return None

def testRun():
    print("bro")