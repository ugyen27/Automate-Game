
from multiprocessing.dummy import current_process
import cv2
import mediapipe as mp 
import time 
from directkeys import right_pressed,left_pressed
from directkeys import PressKey, ReleaseKey

break_Key_pressed=left_pressed
accelerato_Key_pressed = right_pressed

time.sleep(2.0)
current_Key_pressed=set()

mp_draw=mp.solutions.drawing_utils
mp_hand=mp.solutions.hands

tipIds=[4,8,12,16,20]
video = cv2.VideoCapture(0)

with mp_hand.Hands(min_detection_confidence=0.5, 
            min_tracking_confidence=0.5) as hands:
    while True:
        Key_Pressed= False
        break_pressed = False
        accelerator_pressed=False
        key_count=0
        Key_pressed=0
        ret,image=video.read()
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        image.flags.writeable=False
        results=hands.process(image)
        image.flags.writeable=True
        image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        lmList=[]
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands=results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h,w,c=image.shape
                    cx,cy = int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy])

                mp_draw.draw_landmarks(image,hand_landmark,mp_hand.HAND_CONNECTIONS)

        fingers =[]
        if len(lmList)!=0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1,5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            total = fingers.count(1)
            if total == 0:
                cv2.rectangle(image,(20,300),(270,425),(0,255,0),cv2.FILLED)
                cv2.putText(image, "BRAKE", (45,375), cv2.FONT_HERSHEY_SIMPLEX,
                2,(255,0,0),5)
                PressKey(break_Key_pressed)
                break_pressed =True
                current_Key_pressed.add(break_Key_pressed)
                Key_pressed = break_Key_pressed
                Key_Pressed=True
                key_count = key_count+1

            elif total == 5 :
                cv2.rectangle(image,(20,300),(270,425),(0,255,0),cv2.FILLED)
                cv2.putText(image, "BOOSTING....", (45,375), cv2.FONT_HERSHEY_SIMPLEX,
                2,(255,0,0),5)
                PressKey(accelerato_Key_pressed)
                Key_pressed=accelerato_Key_pressed
                accelerator_pressed=True
                break_pressed =True
                Key_Pressed=True
                current_Key_pressed.add(accelerato_Key_pressed)
                key_count = key_count+1

            if not Key_pressed and len(current_Key_pressed) != 0:
                for key in current_Key_pressed:
                    ReleaseKey(key)
                current_Key_pressed = set()
            elif key_count==1 and len(current_Key_pressed)==2:
                for key in current_Key_pressed:
                    if Key_pressed != key:
                        ReleaseKey(key)
                current_Key_pressed = set()
                for key in current_Key_pressed:
                    ReleaseKey(key)
                current_Key_pressed=set()
            
                        # if lmList[8][2] < lmList[6][2]:
            #     print("open")
            # else:
            #     print("close")    
        cv2.imshow("Frame", image)
        k=cv2.waitKey(1)
        if k == ord('q'):
            break
video.release()
cv2.destroyAllWindows()

