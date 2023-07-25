import vgamepad as vg
import time
gamepad = vg.VX360Gamepad()

def move_left_stick(angle):
    val = int(284.8696*angle - 1424.348)
    gamepad.left_joystick(x_value=val, y_value=0)
    gamepad.update()
    time.sleep(0.001)

def move_right_stick(angle):
    val = int(284.8696*angle - 1424.348)
    gamepad.right_joystick(x_value=val, y_value=0)
    gamepad.update()
    time.sleep(0.001)

def accelerate():
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    gamepad.right_trigger(value=255)  # value between 0 and 255
    gamepad.update()

def x_brake():
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    gamepad.update()
    

def neutral():
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    gamepad.right_trigger(value=0)  # value between 0 and 255
    gamepad.update()
    
