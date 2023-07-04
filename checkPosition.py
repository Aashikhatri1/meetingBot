import pyautogui
import time

# Wait for 5 seconds
time.sleep(5)

# Get the current mouse cursor position
position = pyautogui.position()

print("Current mouse position:", position)
