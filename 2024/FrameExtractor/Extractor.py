import os
import cv2
pathOut = r"\FrameExtractor\out\current"
count = 0
counter = 1

vid = r"/FrameExtractor\in\currentMeasurement.mp4"
cap = cv2.VideoCapture(vid)
count = 0
counter += 1
success = True
while success:
    success, image = cap.read()
    print('read a new frame:', success)
    if success and count % 30 == 0:
        cv2.imwrite(pathOut + 'frame%d.jpg' % count, image)
    count += 1