# meet audio recording code
import pyautogui
import cv2
import numpy as np
import time
import webbrowser

#This function will find the image on the screen and return its position
def locate_on_screen(image_path, confidence=0.99):
    # capture the screen
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # read the image file
    template = cv2.imread(image_path, 0)
    
    # convert the screenshot to grayscale
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # match the template with the screenshot
    match = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)

    # if the match is not good enough return None
    if max_val < confidence:
        return None

    return max_loc

# This function will click on the center of an image on the screen
def click_on_image(image_path):
    loc = locate_on_screen(image_path)

    if loc is not None:
        # get the size of the image
        img = cv2.imread(image_path)
        h, w, _ = img.shape

        # calculate the center of the image
        center = (loc[0] + w // 2, loc[1] + h // 2)

        # move the cursor to the center of the image and click
        pyautogui.moveTo(center)
        pyautogui.click()
        return True
    else:
        return False

time.sleep(2)
    # Click on the microphone button
#if not locate on screen(r'meetbot_images\meeting_end_button.png', confidence=0.9):
  #  print("Couldn't find the microphone button")
if not click_on_image(r'meetbot_images\meeting_end_button.png'):
    print("Couldn't find the microphone button")
    
    

#join_meeting('abc', link, 'line1')
