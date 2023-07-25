import mediapipe as mp
import cv2
import numpy as np
from directkeys import W, A, S, D, PressKey, ReleaseKey
from updatedgame import get_label, calculate_steering_angle, speed_control, steer, acceleration, brake, hands_are_open
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5, max_num_hands=2) as hands: 
    while cap.isOpened():
        ret, frame = cap.read()
        # Getting Video Frame Dimensions
        
        # BGR 2 RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Flip on horizontal
        image = cv2.flip(image, 1)
        
        # Set flag
        image.flags.writeable = False
        
        # Detections
        results = hands.process(image)
        
        # Set flag to true
        image.flags.writeable = True
        
        # RGB 2 BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        width = int(image.shape[1])

        w1 = width*2//5 - 21
        w2 = w1 + 42
      
        # Rendering results
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS, 
                                        mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                        mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                         )
                
                # Render left or right detection
                if get_label(num, hand, results):
                    text, coord = get_label(num, hand, results)

                    hands_present = len(results.multi_handedness) > 0

                    left_wrist = None
                    right_wrist = None
                    mid_point = None
                    angle = None

                    for idx, classification in enumerate(results.multi_handedness):
                        hand_landmarks = results.multi_hand_landmarks[idx]
                        
                        if classification.classification[0].index == 0 and hands_present:
                            left_wrist = np.array((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x, hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y))
                            left_thumb_tip = np.array((hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x, hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y))
                            left_index_finger_tip = np.array((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x, hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y))
                            left_index_finger_dip = np.array((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x, hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y))
                            left_index_finger_pip = np.array((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x, hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y))

                            x1 = int((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x)*640)
                            y1 = int((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)*480)

                            ltx = int(left_thumb_tip[0]*640)
                            lty = int(left_thumb_tip[1]*480)

                            lfx = int(left_index_finger_tip[0]*640)
                            lfy = int(left_index_finger_tip[1]*480)

                            lpx = int(left_index_finger_pip[0]*640)
                            lpy = int(left_index_finger_pip[1]*480)

                            ldx = int(left_index_finger_dip[0]*640)
                            ldy = int(left_index_finger_dip[1]*480)

                            image = cv2.circle(image, (x1, y1), 15, (255, 255, 255), cv2.FILLED)
                    

                        if classification.classification[0].index == 1 and hands_present:
                            right_wrist = np.array((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x, hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y))
                            right_thumb_tip = np.array((hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x, hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y))
                            right_index_finger_tip = np.array((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x, hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y))
                            right_index_finger_dip = np.array((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x, hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y))
                            right_index_finger_pip = np.array((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x, hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y))


                            x2 = int((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x)*640)
                            y2 = int((hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y)*480)

                            rtx = int(right_thumb_tip[0]*640)
                            rty = int(right_thumb_tip[1]*480)

                            rfx = int(right_index_finger_tip[0]*640)
                            rfy = int(right_index_finger_tip[1]*480)

                            rpx = int(right_index_finger_pip[0]*640)
                            rpy = int(right_index_finger_pip[1]*480)

                            rdx = int(right_index_finger_dip[0]*640)
                            rdy = int(right_index_finger_dip[1]*480)

                            image = cv2.circle(image, (x2, y2), 15, (255, 255, 255), cv2.FILLED)
                    
                        if left_wrist is not None and right_wrist is not None:
                            mid_point = np.array(((left_wrist[0] + right_wrist[0]) / 2, (left_wrist[1] + right_wrist[1]) / 2))
                            mx1 = int(mid_point[0]*640)
                            my1 = int(mid_point[1]*480)
                            image = cv2.circle(image, (mx1, my1), 15, (255, 255, 255), cv2.FILLED)

       
                            acc = ((rtx-rpx)**2+(rty-rpy)**2)**0.5
                            rd1 = ((rfx-x2)**2+(rfy-y2)**2)**0.5
                            rd2 = ((rdx-x2)**2+(rdy-y2)**2)**0.5
                            acc_angle = calculate_steering_angle(rtx,rty,rpx,rpy)
                            rpm = acceleration(rd1,rd2, acc, acc_angle)

                            brk = ((ltx-lpx)**2+(lty-lpy)**2)**0.5
                            ld1 = ((lfx-x1)**2+(lfy-y1)**2)**0.5
                            ld2 = ((ldx-x1)**2+(ldy-y1)**2)**0.5
                            brk_angle = calculate_steering_angle(ltx,lty,lpx,lpy)
                            rev = brake(ld1,ld2, brk)
                            
                            hands_flag = hands_are_open(ld1,ld2,rd1,rd2)

                            if hands_flag == True:
                                ReleaseKey(W)
                                ReleaseKey(A)
                                ReleaseKey(S)
                                ReleaseKey(D) 
                                angle = 0
                            else:
                                angle = calculate_steering_angle(x1,y1,x2,y2)
                            steer(angle)
                            speed_control(rpm, rev)
                            
                        # if left_wrist is not None:
                    
                    # cv2.putText(image, text, coord, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        else:
            ReleaseKey(W)
            ReleaseKey(A)
            ReleaseKey(S)
            ReleaseKey(D)            
            
        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()