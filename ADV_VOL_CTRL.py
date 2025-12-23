import cv2 
import time
import numpy as np
import HandTrackingModule as htm
import math
from pycaw.pycaw import AudioUtilities

#################################
wCam, hCam = 720, 480
#################################  

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon = 0.7, maxHands = 1)

device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
area = 0
colorVol = (255, 0, 0)


while True:
    success, img = cap.read()

    
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=True)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])//100
        # print(area)
        if 300 < area <2000:
            # print("Yes")

            length, img, lineInfo = detector.findDistance(4,8, img)
            print(length)

          
            vol = np.interp(length,[50, 230], [minVol, maxVol])
            volBar = np.interp(length,[50, 230], [400, 150])
            volPer = np.interp(length,[50, 230], [0, 100])
            # clamp percentage and set system volume using scalar API (0.0-1.0)
            volPer = max(0, min(volPer, 100))
            smoothness = 10
            volPer = smoothness * round (volPer/smoothness) 

            fingers = detector.fingersUp()
            # print(fingers)

            if not fingers[4]:
               volume.SetMasterVolumeLevelScalar(volPer/100, None)
               cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
               colorVol = (0, 255, 0)
            else:
                colorVol = (255, 0, 0)



             
    #Drawing 
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 2)     
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0,), cv2.FILLED)   
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)  
    cVol = int(volume.GetMasterVolumeLevelScalar()*100)     
    cv2.putText(img, f'Vol Set: {int(cVol)} %', (380, 50), cv2.FONT_HERSHEY_COMPLEX, 1, colorVol, 2)    

                                
    #Frame rates 
    cTime = time.time()
    fps = 1 / (cTime - pTime) 
    pTime = cTime 

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                                          
    cv2.imshow("Main webcam", img) 
    cv2.waitKey(1)

