import numpy as np
import cv2
import glob
import os
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*8,3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob('nichols/*.jpg')

def im_show(img, time):
    cv2.namedWindow("img")
    cv2.moveWindow("img", 0,100)
    cv2.imshow("img", img)
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''') 
    cv2.waitKey(time)


for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (8,6), None)
    print(ret)
    # If found, add object points, image points (after refining them)
    if ret == True:
        print("hi!")
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners, (5,5), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv2.drawChessboardCorners(img, (8,6), corners2, ret)
        # im_show(img, 10)


ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

for fname in images:
    img = cv2.imread(fname)
    h,  w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))
    print(newcameramtx.dtype)
    np.savetxt('calibration.txt', mtx)
    np.savetxt('calibration2.txt', dist)
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    x, y, w, h = roi
    # print(w)
    # print(h)
    # dst = dst[y:y+h, x:x+w]
    im_show(dst, 10)


cam = cv2.VideoCapture(2)

while True:
    img = cam.read()[1]
    img = cv2.flip(img, 0)
    h,  w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imshow('calibresult.png', dst)
    a = cv2.waitKey(100)
    if a == ord('q'):
        break
    elif a == ord(" "):
        cv2.imwrite("usergen/img" + str(int(time.time())) + ".jpg", frame)
