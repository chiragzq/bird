import numpy as np
import cv2
import glob
import os
import time

# def im_show(img, time):
#     cv2.namedWindow("img")
#     cv2.moveWindow("img", 0,100)
#     cv2.imshow("img", img)
#     os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''') 
#     cv2.waitKey(time)

# load video source
cam = cv2.VideoCapture(2)

while True:
    frame = cam.read()[1]
    print(frame.shape)
    # display image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # flip gray image vertically
    gray = cv2.flip(gray, 0)

    cv2.imshow("im", gray)
    a = cv2.waitKey(1)
    if a == ord('q'):
        break
    elif a == ord(" "):
        cv2.imwrite("nichols/img" + str(int(time.time())) + ".jpg", gray)