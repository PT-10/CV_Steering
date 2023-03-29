import cv2
import mediapipe as mp
import numpy as np

drawingModule = mp.solutions.drawing_utils
handsModule = mp.solutions.hands

# Define video capture device
capture = cv2.VideoCapture(0)



def calculate_steering_angle(landmark_list):
    # Get coordinates of thumb and index finger
    thumb_x, thumb_y = landmark_list[4][1], landmark_list[4][2]
    index_x, index_y = landmark_list[8][1], landmark_list[8][2]

    # Calculate angle between thumb and index finger
    angle = np.arctan2(index_y - thumb_y, index_x - thumb_x)

    # Convert angle to degrees and return
    return np.degrees(angle)

 

#Instantiating an object of class hands
with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:
 
    while (True):
 
        ret, frame = capture.read()

        #hands.process(frame) gives and output in BGR format but to draw landmarks on the hand in each frame the frame has to be in RGB format which is why we convert it
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            for idx, handLandmarks in enumerate(results.multi_hand_landmarks):
                drawingModule.draw_landmarks(frame, handLandmarks, handsModule.HAND_CONNECTIONS)

            # left_hand_landmarks = []
            # right_hand_landmarks = []

            # if results.multi_handedness[idx].classification[0].label == "Left":
            #     for idx, landmark in enumerate(handLandmarks.landmark):
            #         # Store landmarks for left hand in the left_hand_landmarks array
            #         left_hand_landmarks.append([idx, landmark.x, landmark.y, landmark.z])
            # else:
            #     for idx, landmark in enumerate(handLandmarks.landmark):
            #         # Store landmarks for right hand in the right_hand_landmarks array
            #         right_hand_landmarks.append([idx, landmark.x, landmark.y, landmark.z])
            # print(right_hand_landmarks[0][1])
            # print(left_hand_landmarks[0][1])
            # #A landmark list is created for each frame to store the coodinates of all landmarks as a 2D array
            landmark_list = []
            for idx, landmark in enumerate(handLandmarks.landmark):
                landmark_list.append((idx, landmark.x, landmark.y, landmark.z))

            # Calculate steering angle based on hand landmarks
            # Replace this with your own gesture recognition model
            steering_angle = calculate_steering_angle(landmark_list)

            #Convert steering angle to digital value
            # digital_value = int((steering_angle + 45) / 90 * 255)

            #Print digital value to console
            print("Steering angle for each frame's gesture is:", steering_angle)
 
        cv2.imshow('Test hand', frame)
 
        if cv2.waitKey(1) == 27:
            break
 
cv2.destroyAllWindows()
capture.release()
