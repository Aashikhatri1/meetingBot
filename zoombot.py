from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import cv2
import numpy as np
import pyautogui
import time
from time import sleep
import sys
import os

# Fetch the meeting link from the command line arguments
if len(sys.argv) > 1:
    meeting_link = sys.argv[1]
else:
    print("No Zoom link provided. Exiting.")
    sys.exit(1)
    
# Open the browser
# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Disable popup for allowing webcam and microphone
chrome_options.add_argument("--disable-notifications")  # Disable notifications
chrome_options.add_argument("--start-maximized")  # Open browser in maximized mode

chrome_options.add_experimental_option('prefs', {
  "protocol_handler": {
    "excluded_schemes": {
      "zoommtg": False
    }
  }
})

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Navigate to the meeting
driver.get(meeting_link)

time.sleep(6)  # wait for the page to load

# This function will find the image on the screen and return its position
def locate_on_screen(image_path, confidence=0.4):
    if not os.path.exists(image_path):
        print(f"The image file '{image_path}' does not exist.")
        return None

    # capture the screen
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # save screenshot for debugging
    cv2.imwrite('debug_screenshot.png', screenshot)

    # read the image file
    template = cv2.imread(image_path, 0)

    # convert the screenshot to grayscale
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    best_match_val = 0
    best_match_loc = None

    # scales for template matching
    scales = np.linspace(0.2, 1.0, 20)[::-1]

    # perform template matching at different scales
    for scale in scales:
        # resize the image according to the scale
        resized_template = cv2.resize(template, None, fx=scale, fy=scale)

        # if the resized image is smaller than the template, then break from the loop
        if resized_template.shape[0] > gray_screenshot.shape[0] or resized_template.shape[1] > gray_screenshot.shape[1]:
            break

        # match the resized template with the screenshot
        match = cv2.matchTemplate(gray_screenshot, resized_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(match)
        print(f"Scale: {scale}, Match value: {max_val}")
        

        # if this max value is greater than the best match value, update best match value and best match location
        if max_val > best_match_val:
            best_match_val = max_val
            best_match_loc = max_loc

    # if the best match value is less than the confidence, return None
    if best_match_val < confidence:
        print(f"No match for '{image_path}' found on screen. Max match value is {best_match_val}.")
        return None
        
    print(f"Image '{image_path}' found on screen with confidence {best_match_val}.")
    return best_match_loc

# This function will click on the given position of an image on the screen
def click_on_image(image_path, position='center'):
    loc = locate_on_screen(image_path)

    if loc is None:
        print(f"Unable to locate image '{image_path}' on screen.")
        return False

    if loc is not None:
        # get the size of the image
        img = cv2.imread(image_path)
        h, w, _ = img.shape

        if position == 'top-right':
            # calculate the top right corner of the image
            # click_position = (loc[0] + w-1, loc[1])
            click_position = (loc[0] + w - 11, loc[1] + 10)
        elif position == 'bottom-center':
            # calculate the bottom center of the image
            click_position = (loc[0] + w // 2, loc[1] + h-10)
        elif position == 'right-center':
        # calculate the right-center of the image
            click_position = (loc[0] + w, loc[1] + h // 2)
        else:
            # calculate the center of the image
            click_position = (loc[0] + w // 2, loc[1] + h // 2)

        # move the cursor to the click_pos of the image and click
        pyautogui.moveTo(click_position)
        pyautogui.click()
        return True
    else:
        return False


# The main function to join a meeting
def join_meeting(meeting_link): 
    time.sleep(7)
    if not click_on_image(r'zoombot_images\accept_cookies_button.png'):
        print("Couldn't find the accept_cookies_button")
        return
    
    time.sleep(1)
    
    click_on_image(r'zoombot_images\keep_button.png')
    
    time.sleep(4)

    click_on_image(r'zoombot_images\launch_meeting_button.png')
    
    time.sleep(5)

    click_on_image(r'zoombot_images\browser_button.png')

    time.sleep(5)

    click_on_image(r'zoombot_images\agree_button.png')

    time.sleep(5)
    click_on_image(r'zoombot_images\enter_name_button.png')
    
    pyautogui.write('Bot')
    click_on_image(r'zoombot_images\join_button.png')
    time.sleep(10)
    click_on_image(r'zoombot_images\video_button1.png')
    
    time.sleep(2)
    
    # Click on the microphone button to turn it off
    if not click_on_image(r'zoombot_images\mute_button1.png'):
        print("Couldn't find the mute button 1")
        return
        
    # Moving the cursor in the centre of the screen
    screen_width, screen_height = pyautogui.size()                 # Get the screen size
    center_x, center_y = screen_width // 2, screen_height // 2     # Calculate the center of the screen
    pyautogui.moveTo(center_x, center_y)                           # Move the mouse to the center of the screen

    # Move the cursor for n seconds
    start_time = time.time()

    # Loop for 2 seconds
    while time.time() - start_time < 2:
        # Move the mouse cursor by 100 pixels in x and y direction
        pyautogui.move(100, 100, duration=0.25)
        time.sleep(0.25)  # pause a bit before next movement

        # Move the mouse cursor back to initial position
        pyautogui.move(-100, -100, duration=0.25)
        time.sleep(0.25)  # pause a bit before next movement

    # Click on the More options button
    if not click_on_image(r'zoombot_images\more_options_button.png1', 'top-right'):
        print("Couldn't find the more options button 1")
        return
    
    time.sleep(1)
    
    if not click_on_image(r'zoombot_images\audio_settings_button1.png'):
        print("Couldn't find the audio settings button 1")
        return
    
    time.sleep(1)

    while not click_on_image(r'zoombot_images\test_speaker_button1.png', 'right-center'):
        # wait for a bit before trying again
        sleep(1)

    time.sleep(1)

    if not click_on_image(r'zoombot_images\line_1_button1.png'):
        print("Couldn't find the Line 1 button 1")
        return
    
    time.sleep(1)

    if not click_on_image(r'zoombot_images\exit_settings_button1.png','right-center'):
        print("Couldn't find the exit settings button 1")
        return
    
# Call the function with your meeting link
join_meeting(meeting_link)
