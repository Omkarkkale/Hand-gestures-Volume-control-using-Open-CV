import cv2 as cv
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self,mode = False,maxHands = 2, detectionCon = 0.5,trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode= self.mode,
                                        max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence= self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        
        # Tip IDs for the five fingers in MediaPipe (thumb, index, middle, ring, pinky)
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self,img,draw = True):
        imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLM in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLM,self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        lmList = []
        if not hasattr(self, 'results') or not self.results:
            return lmList, bbox
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv.circle(img, (cx, cy), 5, (0, 255, 0), cv.FILLED)
            
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv.rectangle(img,  (bbox[0]-20, bbox[1]-20), (bbox[2]+20, bbox[3]+20), (0, 255, 0), 2)



            # save last landmark list for convenience in other methods
            self.lmList = lmList

        return lmList, bbox

    def distance(self,point1,point2):
        return (point1[1] - point2[1])*(point1[1] - point2[1]) + (point1[2] - point2[2])*(point1[2] - point2[2])

    def getFingers(self,img,handNo = 0):
        fingers = [1,1,1,1,1]
        lmList = self.findPosition(img,handNo= handNo)
        try:
            if abs(lmList[3][1]-lmList[0][1]) < (lmList[2][1]-lmList[0][1]) or self.distance(lmList[0], lmList[2]) > self.distance(lmList[4], lmList[0]):
                fingers[0] = 0
            if self.distance(lmList[0], lmList[6]) > self.distance(lmList[8], lmList[0]):
                fingers[1] = 0
            if self.distance(lmList[0], lmList[10]) > self.distance(lmList[0], lmList[12]):
                fingers[2] = 0
            if self.distance(lmList[0], lmList[14]) > self.distance(lmList[0], lmList[16]):
                fingers[3] = 0
            if self.distance(lmList[0], lmList[18]) > self.distance(lmList[0], lmList[20]):
                fingers[4] = 0
        except:
            raise Exception("NO Hand Found")
        return fingers
    
    def fingersUp(self):
        fingers = []
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range (1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
    
    def findDistance (self, p1, p2, img, draw = True):
            x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
            x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
            cx, cy = (x1 + x2) // 2,  (y1 + y2) // 2 

            if draw:
                cv.circle(img, (x1, y1), 15, (255, 0, 255), cv.FILLED)
                cv.circle(img, (x2, y2), 15, (255, 0, 255), cv.FILLED)
                cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv.circle(img, (cx, cy), 15, (255, 0, 255), cv.FILLED)

            length = math.hypot(x2-x1, y2-y1)
            return length, img, [x1,y1,x2,y2,cx,cy]



def main():
    pTime = 0
    cap = cv.VideoCapture(1)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        try:
            fingers = detector.getFingers(img)
            print(fingers)
        except Exception as ex:
            print(f'An Exception Occurred: {ex}')
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv.imshow('image', img)
        k = cv.waitKey(1)
        if k == 27:
            cv.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
