import numpy as np
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
from directkeys import W, A, S, D, PressKey, ReleaseKey, SensitivePressKey

# Define a global variable for angle smoothing
smoothing_factor = 0.9
smoothed_angle = 0.0

def get_label(index, hand, results):
    output = None
    for idx, classification in enumerate(results.multi_handedness):
        if classification.classification[0].index == index:
            # Process results
            
            label = classification.classification[0].label
            score = classification.classification[0].score
            text = '{} {}'.format(label, round(score, 2))
            
            # Extract Coordinates
            coords = tuple(np.multiply(
                np.array((hand.landmark[mp_hands.HandLandmark.WRIST].x, hand.landmark[mp_hands.HandLandmark.WRIST].y)),
            [640,480]).astype(int))
            
            output = text, coords       
    return output

def hands_are_open(ld1,ld2,rd1,rd2):
    return rd1>rd2 and ld1>ld2

def calculate_steering_angle(x1,y1,x2,y2):
    # Calculate angle 
    angle = np.arctan2(y2 - y1, x2 - x1)
    # Convert angle to degrees and return
    return np.degrees(angle)

def orientation(angle):

    if 10<=angle<=120:
        return "Right"
    if -120<=angle<=-10:
        return "Left"
    if -10<=angle<=10:
        return "Neutral"


def smooth_angle(angle):
    global smoothed_angle
    # Smooth the angle using a simple moving average
    smoothed_angle = smoothing_factor * smoothed_angle + (1 - smoothing_factor) * angle
    return smoothed_angle

    
def steer(angle):
    # Smooth the angle
    angle = smooth_angle(angle)

    res_angle = angle
    # Lock the angle within the defined range
    if angle < -120:
        res_angle = -120
    elif angle > 120:
        res_angle = 120

    
    # print("Original angle",angle)
    nav = orientation(res_angle)
    print("Steering angle", res_angle)
    
    if nav == "Left":
        ReleaseKey(D)
        SensitivePressKey(A, res_angle)
        print("Vehicle steer:",nav)    
    elif nav == "Right":
        ReleaseKey(A)
        SensitivePressKey(D, res_angle)
        print("Vehicle steer:",nav)

    elif nav == "Neutral":
        ReleaseKey(A)
        ReleaseKey(D)
        print("Vehicle steer:",nav)


def acceleration(rd1, rd2, distance, angle):
    if rd1<rd2:
        if 10<=distance<=35 and angle>0:
            return 'Forward'
        else:
            return 'Neutral'
    else:
        print("Close your right hand")


def brake(ld1, ld2, distance):
    if ld1<ld2:
        if 10<=distance<=35 :
            return 'Back'
        else:
            return 'Neutral'  
        
    else:
        print("Close your left hand")

def speed_control(rpm, rev):
    if rpm == "Forward":
        ReleaseKey(S)
        PressKey(W)
        print("Vehicle is on", rpm)
        
    if rev == "Back":
        ReleaseKey(W)
        PressKey(S)
        print("Vehicle is on", rev)

    elif rpm == "Neutral":
        ReleaseKey(S)
        ReleaseKey(W)
        print("Vehicle is on", rpm)

    