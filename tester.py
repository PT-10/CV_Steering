import vgamepad as vg
import time

gamepad = vg.VX360Gamepad()
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.update()
time.sleep(1)
gamepad.left_joystick(x_value=int(284.8696*120 - 1424.348), y_value=0)  # values between -32768 and 32767
gamepad.update()
time.sleep(5)
for i in range(-100,70):
    gamepad.left_joystick(x_value=int(284.8696*i - 1424.348), y_value=0)  # values between -32768 and 32767
    gamepad.update()
    time.sleep(0.01)
time.sleep(2)
gamepad.left_joystick(x_value=int(284.8696*100 - 1424.348), y_value=0)  # values between -32768 and 32767
gamepad.update()
time.sleep(5)
gamepad.left_joystick(x_value=0, y_value=0)  # values between -32768 and 32767
gamepad.update()
time.sleep(2)
