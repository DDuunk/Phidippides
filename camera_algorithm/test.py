import cv2
import roadCoordinator as rd
import math
import numpy as np
# test = rd.RoadCoordinator(200,0,[100,150,0],[140,255,255], [0,0,0], [155, 55, 255], (255,72,0), True)
# cap = cv2.VideoCapture('test.mp4')
test = rd.RoadCoordinator(50, 20, [0,0,0], [255, 120, 255], [0,0,0], [0,0,0], (0,0,0), False)
cap = cv2.VideoCapture('test2.mp4')
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        test.getRoadBorderCoordinates(frame)
        soughtAfterAngle = math.degrees(math.atan((test.middleY / test.middleX)))
        print(soughtAfterAngle)
        cv2.imshow('frame2',frame)

        
        if cv2.waitKey(25) & 0xFF == ord('q'):    
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()