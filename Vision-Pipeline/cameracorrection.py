import cv2 as cv
import numpy as np
"""
Hard coded distortion coefficients and values for the Raspberry Pi Wide Angle camera
"""
dist_coeffs = np.array([-3.33440903e-01,  1.22459385e-01, -1.36736921e-03,  1.50750541e-04,
                        -2.10696063e-02])
    
camera_matrix = np.array([[240.84171937,   0, 343.73323286],
                            [   0, 240.38352732, 223.76385059],
                            [  0,            0,             1         ]])

optimised_camera_matrix = np.array([[240.46542358,   0,         343.19617006],
                                    [  0,   239.88273621, 223.29768298],
                                    [  0,           0,          1           ]])
roi = (0, 0, 639, 479)

def undistort(image) -> any:
    img_undistort = cv.undistort(image, camera_matrix, dist_coeffs, None, optimised_camera_matrix)
    x, y, w, h = roi
    cv.rectangle(img_undistort, (x,y), (x+w, y+h), (0,0,255), 2)
    img_undistort = img_undistort[y:y+h, x:x+w]
    return img_undistort

def main() -> None:
    cam = cv.VideoCapture(1)
    print("width", cam.get(cv.CAP_PROP_FRAME_WIDTH))
    print("height", cam.get(cv.CAP_PROP_FRAME_HEIGHT))
    while True:
        ret, frame = cam.read()
        correctedFrame = undistort(frame)
        cv.imshow("Undistorted", frame)
        cv.imshow("Distorted", correctedFrame)
        k = cv.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
    cam.release()

if __name__ == "__main__":
    main()