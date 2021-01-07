import cv2
import road_coordinator as rd
import math
test = rd.RoadCoordinator(200,0,[100,150,0],[140,255,255])
cap = cv2.VideoCapture('test.mp4')
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        test.getRoadBorderCoordinates(frame)
        soughtAfterAngle = math.degrees(math.atan((test.middleY / test.middleX)))
        print(soughtAfterAngle)
        cv2.imshow('frame',frame)

        
        if cv2.waitKey(25) & 0xFF == ord('q'):    
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()