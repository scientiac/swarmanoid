#!/usr/bin/env python
import numpy as np
import cv2
import glob

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
# size of each square is 35 mm
square_size = 0.0355  # in meters
objp = np.zeros((6 * 9, 3), np.float32)
objp[:, :2] = (square_size * np.mgrid[0:9, 0:6]).T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

images = glob.glob(
    r"./images/*.png",
)

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sample_im = gray
    # cv2.imshow(gray)
    # Find the chess board corners
    chessboard_flags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE
    flags = 0
    flags |= cv2.CALIB_CB_ADAPTIVE_THRESH
    flags |= cv2.CALIB_CB_NORMALIZE_IMAGE
    [ret, corners] = cv2.findChessboardCorners(gray, (9, 6), flags)

    # If found, add object points, image points (after refining them)
    if ret == True:
        # print ('True')
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)  # these are the found corners

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (9, 6), corners2, ret)
        cv2.imshow("img", img)
        cv2.waitKey(100)

cv2.destroyAllWindows()
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)


# Undistortion
# refine the camera matrix
ii = -1
for fname in images:
    # if (fname==images[0]):
    ii += 1
    img = cv2.imread(fname)
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    dst1 = cv2.undistort(img, newcameramtx, dist, None, None)

    # testing if the matrix is right
    image_path1 = r"./images/final/%i.png" % ii
    cv2.imwrite(image_path1, dst1)

path = r"./miatoll.yml"
cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_WRITE)
cv_file.write("new_matrix", newcameramtx)
cv_file.write("distortion_coef", dist)

cv_file.release()

# Re-projection Error
tot_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    tot_error += error

print("total error: ", tot_error / len(objpoints))
