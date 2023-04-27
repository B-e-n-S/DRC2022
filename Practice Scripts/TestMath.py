import math
import numpy as np
import idk
import FinalTest

x = math.pi
print(x)
xdeg = math.degrees(x)
print(xdeg)
xclipped = np.clip(xdeg, 160, 170)
print(xclipped)
# idk.testRun()

def main():
    idk.create_global_variables()
    FinalTest.consolidateUnderstanding()

if __name__ == "__main__":
    print("Initialising...")
    main()


    