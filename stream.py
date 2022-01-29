import numpy as np
import cv2
import glob
import os

def read_img(cam):
    img = cam.read()[1]
    # img = cv2.flip(img, 0)
    return cv2.undistort(img, mtx, dist, None, newcameramtx)

cams = [cv2.VideoCapture(i) for i in [1,2,3]]
img = cams[0].read()[1]
h,  w = img.shape[:2]
mtx = np.loadtxt('calibration.txt', dtype=np.float64)
dist = np.loadtxt('calibration2.txt', dtype=np.float64)
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))


while True:
    imgs = [read_img(cam) for cam in cams]
    # dsts = [cv2.undistort(img, mtx, dist, None, newcameramtx) for img in imgs]
    # dst = cv2.undistort(imgs, mtx, dist, None, newcameramtx)
    x, y, w, h = roi
    # dsts = [dst[y:y+h, x:x+w] for dst in dsts]
    joined = np.concatenate(imgs, axis=1)

    cv2.imshow('calibresult.png', joined)
    a = cv2.waitKey(1)
    if a == ord('q'):
        break
    # elif a == ord(" "):
    #     cv2.imwrite("usergen/img" + str(int(time.time())) + ".jpg", frame)
