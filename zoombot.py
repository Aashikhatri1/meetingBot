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
def locate_on_screen(image_path, confidence=0.8):
    # capture the screen
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # read the image file
    templ = cv2.imread(image_path, 0)
    
    # Get dimensions of images
    h_img, w_img = screenshot.shape[:2]  # source image
    h_templ, w_templ = templ.shape[:2]  # template image

    # Check if source image dimensions are larger than template dimensions
    if (h_img < h_templ) or (w_img < w_templ):
        print('Template dimensions are larger than source image. Please resize the template or choose a smaller one.')
        return None

    # convert the screenshot to grayscale
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # match the template with the screenshot
    match = cv2.matchTemplate(gray_screenshot, templ, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)

    # if the match is not good enough return None
    if max_val < confidence:
        return None

    return max_loc


# This function will click on the given position of an image on the screen
def click_on_image(image_path, position='center'):
    loc = locate_on_screen(image_path)

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

    click_on_image(r'zoombot_images\allow_button.png')
    click_on_image(r'zoombot_images\allow_button1.png')
    click_on_image(r'zoombot_images\cookies_button.png', 'top-right')
    click_on_image(r'zoombot_images\cross_button.png','top-right')
    
    time.sleep(2)
    click_on_image(r'zoombot_images\exit_login_button.png', 'top-right')
    
    time.sleep(2)

    click_on_image(r'zoombot_images\launch_meeting_button.png')
    
    time.sleep(5)

    click_on_image(r'zoombot_images\cross_button.png','top-right')
    click_on_image(r'zoombot_images\exit_login_button.png', 'top-right')
    time.sleep(2)

    click_on_image(r'zoombot_images\browser_button.png')

    # _____________
    
    # Define a start time
    start_time = time.time()

    # Loop until the audio button appears or 50 seconds have passed
    while not click_on_image(r'zoombot_images\computer_audio_button.png') and time.time() - start_time < 120:
        # wait for a bit before trying again
        sleep(5)

    # If the computer audio button did not appear within 50 seconds, perform the alternative actions
    if time.time() - start_time >= 120:
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

        # Rest of the alternative actions...
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

    else:
    # Continue with the regular actions if the computer audio button appeared within 50 seconds
        click_on_image(r'zoombot_images\maximize_button.png')
    

        start_time = time.time()

        # Loop for 2 seconds
        while time.time() - start_time < 2:
            # Move the mouse cursor by 100 pixels in x and y direction
            pyautogui.move(100, 100, duration=0.25)
            time.sleep(0.25)  # pause a bit before next movement

            # Move the mouse cursor back to initial position
            pyautogui.move(-100, -100, duration=0.25)
            time.sleep(0.25)  # pause a bit before next movement

        click_on_image(r'zoombot_images\video_button.png')
        
        time.sleep(2)
        
        # Click on the microphone button to turn it off
        if not click_on_image(r'zoombot_images\mute_button.png'):
            print("Couldn't find the mute button")
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
        if not click_on_image(r'zoombot_images\more_options_button.png', 'top-right'):
            print("Couldn't find the more options button")
            return
        
        time.sleep(1)
        
        if not click_on_image(r'zoombot_images\audio_settings_button.png'):
            print("Couldn't find the audio settings button")
            return
        
        time.sleep(1)

        while not click_on_image(r'zoombot_images\test_speaker_button.png', 'right-center'):
            # wait for a bit before trying again
            sleep(1)

        time.sleep(1)

        if not click_on_image(r'zoombot_images\line_1_button.png'):
            print("Couldn't find the Line 1 button")
            return
        
        time.sleep(1)

        if not click_on_image(r'zoombot_images\exit_settings_button.png','right-center'):
            print("Couldn't find the exit settings button")
            return
    
# Call the function with your meeting link
join_meeting(meeting_link)
