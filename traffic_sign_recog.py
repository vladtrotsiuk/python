# -*- coding: utf-8 -*-
import cv2 as cv
#import numpy as np
#cap = cv.VideoCapture('2019_000388519715.avi')
#cap = cv.VideoCapture(0)
cap = cv.VideoCapture('video_file_name')
while (True):
    ret,frame = cap.read()
    cv.imshow("Frame", cv.resize(frame, (640, 360)))

    last_red_frame = None
    last_green_frame = None
    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    hsv = cv.blur(hsv,(5,5))

    red_mask1 = cv.inRange(hsv, (0, 85, 110), (15, 255, 255))
    red_mask2 = cv.inRange(hsv, (165, 85, 110), (180, 255, 255))
    red_mask = red_mask1 + red_mask2
    green_mask = cv.inRange(hsv, (40, 85, 110), (91, 255, 255))
    
    
    countours = cv.findContours(red_mask,cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    countours = countours[1]
    cv.drawContours(frame, countours, -1, (255, 0, 255), 3)
    for cont in countours:
        (x, y, w, h) = cv.boundingRect(cont)
        cv.rectangle(frame,(x,y),(x+2*w, y+5*h), (0,255,0), 2)
        cv.imshow("rect", cv.resize(frame, (640, 360)))
        
    
        
    if last_red_frame is None:
        last_red_frame = red_mask
    if last_green_frame is None:
        last_green_frame = green_mask

    red_dif_frame = (last_red_frame - red_mask)
    green_dif_frame = (green_mask - last_green_frame)
    ret, red_dif_frame = cv.threshold(red_dif_frame, 127, 255, cv.THRESH_BINARY)
    ret, green_dif_frame = cv.threshold(green_dif_frame, 127, 255, cv.THRESH_BINARY)
 
    last_green_frame = green_mask
    last_red_frame = red_mask

    res_red = cv.bitwise_and(frame, frame, mask=red_mask)
    res_green = cv.bitwise_and(frame, frame, mask=green_mask)
    res_all = res_green + res_red
    #cv.imshow("res_all", cv.resize(res_all, (640, 360)))
    if cv.waitKey(1) == ord("q"):
        break
    
cap.release()
cv.destroyAllWindows()