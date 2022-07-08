import cv2 as cv
import numpy as np
import os
import glob

#Main Camera Calibration File

def get_chessboard_corners(board, board_size: tuple) -> np.ndarray:
    """
    Returns an array of corners for the provided board if found, else None.
    """

    board_gray = cv.cvtColor(board, cv.COLOR_BGR2GRAY)

    flag = cv.CALIB_CB_EXHAUSTIVE + cv.CALIB_CB_NORMALIZE_IMAGE
    found, corners = cv.findChessboardCornersSB(board_gray, board_size, None, flag)
    cv.imshow('img', board_gray)
    cv.waitKey(100)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    print(found)
    if found:
        corners2 = cv.cornerSubPix(board_gray, corners, (11,11), (-1,-1), criteria)
        cv.drawChessboardCorners(board, board_size, corners2, found)
        cv.imshow('img', board)
        cv.waitKey(100)
        return corners2
    return None

def get_points(img_dir: str, board_size: tuple) -> tuple:
    """
    Finds object points (3D) and image points (2D) for all chessboard images in the provided directory.
    """
    img_total = len(os.listdir(img_dir))
    h, w = board_size

    # prepare object points
    objp = np.zeros((h*w,3), np.float32)
    objp[:,:2] = np.mgrid[0:h,0:w].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    # Collect corners from images
    #images = glob.glob('C:/Users/b3nsc/OneDrive - The University of Sydney (Students)/Documents/University/Societies/Robotics/OpenCVPractice/calibration2/*.jpg')

    #for image in images:
    for i in range(0, img_total):
        chessboard = cv.imread(f"{img_dir}/opencv_frame_{i}.png")
        #chessboard = cv.imread(image)
        corners = get_chessboard_corners(chessboard, board_size)
        img_size = chessboard.shape[::-1][-2:]
        success = False
        if not (corners is None):
            objpoints.append(objp)
            imgpoints.append(corners)
            success = True
            print("Working")

        # Draw the corners
        cv.drawChessboardCorners(chessboard, (board_size[0], board_size[1]), corners, success)
        
        # Display the image. Used for testing.
        #cv.imshow("Image", chessboard) 
        print("Image should be showing")
        # Display the window for a short period. Used for testing.
        #cv.waitKey(10) 
    print(imgpoints)
    return objpoints, imgpoints, img_size

def undistort(image) -> any:
    """
    Hard coded distortion coefficients and values for the Raspberry Pi Wide Angle camera
    """
    dist_coeffs = np.array([-2.82695785e-01, 8.26604087e-02, -1.97719384e-04,
                            -1.47684094e-04, -1.09232951e-02])
    
    camera_matrix = np.array([[294.83371528,   0,           330.31339406],
                              [  0,          294.33297786,  227.43893483],
                              [  0,            0,             1         ]])

    optimised_camera_matrix = np.array([[294.37304688,   0,         329.79729973],
                                        [  0,         293.7197876,  226.96510898],
                                        [  0,           0,          1           ]])
    
    return cv.undistort(image, camera_matrix, dist_coeffs, None, optimised_camera_matrix)

def main() -> None:
    image_dir = "./ChessBoardCaptures"
    board_size = (5, 8)
    board_size_reduced = (board_size[0]-1, board_size[1]-1)
    print(board_size_reduced)
    # # Calculate distortion matrix
    objpoints, imgpoints, img_size = get_points(image_dir, board_size_reduced)
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, img_size, None, None)
    newMtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, img_size, 0, img_size)

    # Open distorted image
    img = cv.imread(f"{image_dir}/opencv_frame_6.png")
    img_undistort = cv.undistort(img, mtx, dist, None, newMtx)
    print("mtx", mtx)
    print("dist", dist)
    print("newMtx", newMtx)
    print("roi", roi)
    #img_undistort = undistort(img)

    # Bounding box of real roi when alpha == 0
    x, y, w, h = roi
    cv.rectangle(img_undistort, (x,y), (x+w, y+h), (0,0,255), 2)
    img_undistort = img_undistort[y:y+h, x:x+w]

    cv.imshow("Undistorted", img_undistort)
    cv.imshow("Distorted", img)
    cv.waitKey(0)

if __name__ == "__main__":
    main()