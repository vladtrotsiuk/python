import cv2 as cv
#import numpy as np
cap = cv.VideoCapture('2019_000389151653.avi')
#cap = cv.VideoCapture(0)
#cap = cv.VideoCapture('video_file_name')
last_red_frame = None
last_green_frame = None
count = 0
while (True):
    ret,frame = cap.read()
#    cv.imshow("Frame", cv.resize(frame, (640, 360)))
    count += 1
    
    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    hsv = cv.blur(hsv,(5,5))

    red_mask1 = cv.inRange(hsv, (0, 85, 110), (15, 255, 255))
    red_mask2 = cv.inRange(hsv, (165, 85, 110), (180, 255, 255))
    red_mask = red_mask1 + red_mask2
    green_mask = cv.inRange(hsv, (40, 85, 110), (91, 255, 255))
    
    
    if last_red_frame is None:
        last_red_frame = red_mask
    if last_green_frame is None:
        last_green_frame = green_mask
    if count%3 == 0:
        red_dif_frame = (last_red_frame - red_mask)
        green_dif_frame = (green_mask - last_green_frame)
        ret, red_dif_frame = cv.threshold(red_dif_frame, 127, 255, cv.THRESH_BINARY)
        ret, green_dif_frame = cv.threshold(green_dif_frame, 127, 255, cv.THRESH_BINARY)
    
        copy = red_dif_frame.copy()
    
        
        countours = cv.findContours(green_mask,cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        countours = countours[1]
        cv.drawContours(frame, countours, -1, (255, 0, 255), 3)
        for cont in countours:
            (x, y, w, h) = cv.boundingRect(cont)
            if cv.countNonZero(green_mask[y:y+h, x:x+w]) > 200:
                cv.rectangle(frame,(x-w,y-3*h),(x+w+5, y+h+5), (0,255,0), 2)

            if cv.countNonZero(green_mask[y:y+h, x:x+w]) > 100 and cv.countNonZero(red_mask[y-3*h:y-h, x-w:x+w])-cv.countNonZero(last_red_frame[y-3*h:y-h, x-w:x+w])<-50 and cv.countNonZero(green_mask[y:y+h, x:x+w])-cv.countNonZero(last_green_frame[y:y+h, x:x+w])>50:
                print('Время видео')

    
        last_green_frame = green_mask
        last_red_frame = red_mask     
        cv.imshow("rect", cv.resize(frame, (640, 360)))
    if cv.waitKey(1) == ord("q"):
        break
    
cap.release()
cv.destroyAllWindows()