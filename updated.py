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


def calculate_steering_angle(x1,y1,x2,y2):
    # Calculate angle 
    angle = np.arctan2(y2 - y1, x2 - x1)
    # Convert angle to degrees and return
    return np.degrees(angle)

def orientation(angle):

    if 5<=angle<=120:
        return "Right"
    if -120<=angle<=-5:
        return "Left"
    if -5<=angle<=5:
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

    print("Original angle",angle)
    nav = orientation(res_angle)
    print("Command executed on", res_angle)
    
    if nav == "Left":
        ReleaseKey(D)
        SensitivePressKey(A, res_angle)
        print("Vehicle is on",nav)    
    elif nav == "Right":
        ReleaseKey(A)
        SensitivePressKey(D, res_angle)
        print("Vehicle is on",nav)


def acceleration(rd1, rd2, distance, angle):
    if rd1<rd2:
        if 10<=distance<=35 and angle>0:
            return 'Forward'
        else:
            return 'Neutral'
    else:
        print("Close your right fingers")


def brake(ld1, ld2, distance):
    if ld1<ld2:
        if 10<=distance<=35 :
            return 'Back'
        else:
            return 'Neutral'  
        
    else:
        print("Close your left fingers")

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

    
    
# def direction(x1, w1): 
    
#     if x1<=w1:
#         return "Back"
#     if w1+42<x1:
#         return "Forward"
#     if w1 < x1 < w1+42:
#         return "Neutral"

    