<!-- GETTING STARTED -->
## Getting Started

To set up a local copy up and running follow these steps.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/PT-10/CV_Steering.git
   ```
2. Enter current directory
   ```sh
   cd CV_Steering
   ```
3. Install the requirements:
   ```sh
   pip install mediapipe
   ```
   ```sh
   pip install opencv-python
   ```

<!-- PROJECT OVERVIEW -->
## Project Overview
This project enables you to control your game using gesture steering.
### Repository Structure
The folder consists of four files, hands.py, functions.py, directkeys.py
#### hands.py
* Main python file, consists of the hand tracking module and execution of functions.

#### functions.py
* Currently provides functionality for steering left and right, acceleration and brake.

#### directkeys.py
* Contains the functions to map gestures with key presses.

#### updated.py
* Copy of functions.py with certain improvements

### Configuring Steering Sensitivity
* Adjust the steering sensitivity by modifying the f(angle) function in directkeys.py
  ```
  def f(angle):
    duration = coefficient*abs(angle)
    return duration
  ```
* Original coefficient = 0.002
* Increasing the value increases steering sensitivity.

## Unlock gesture steering
* In your terminal, run:
  ```
  python hands.py
  ```
* The camera module should come up. Run the game you wish to play.


<!-- UNDERSTANDING GESTURES -->
## Understanding the Gestures
### Steering
Hold your hands as if you were gripping a real steering wheel, with your wrists parallel to each other.
The car will maintain its direction when your hands are horizontal. To turn the car, rotate your hands in the respective direction as if turning a steering wheel.

### Acceleration and Brake
Acceleration and brake actions are analogous to pressing a button. To accelerate, touch your right thumb tip against your index finger's pip (the upper joint). To disengage acceleration, move your thumb away while keeping your hand in a thumbs-up position. For braking, use the same gestures with your left hand.


### Under development
* Update 21-07-2023: Time to revive this
* Update 23-07-2023: Revived, usable irl but still rough, supported only on Windows

### Future improvements:
- [ ] Improve landmark detection confidence and reliability, better physics for steering
- [X] Map to controller analog stick instead of keyboard keys
- [ ] Replace brake with nitro and implement aircraft lever method for brake
- [ ] Use mediapipe gestures instead of handlandmarks
