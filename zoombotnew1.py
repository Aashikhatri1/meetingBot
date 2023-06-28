from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import cv2
import numpy as np
import pyautogui
import time
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

time.sleep(7)  # wait for the page to load

# List of images to find on the screen
images = ['zoombot_images\\accept_cookies_button.png',
          'zoombot_images\\discard_button.png',
          'zoombot_images\\launch_meeting_button.png', 'zoombot_images\\browser_button_2.png',
          'zoombot_images\\agree_button.png', 'zoombot_images\\enter_name_button.png',
          'zoombot_images\\join_button.png', 'zoombot_images\\video_button1.png',
          'zoombot_images\\mute_button1.png', 'zoombot_images\\more_options_button.png',
          'zoombot_images\\audio_settings_button1.png', 'zoombot_images\\test_speaker_button1.png',
          'zoombot_images\\line_1_button1.png', 'zoombot_images\\exit_settings_button1.png',
          'zoombot_images\\maximize_button.png', 'zoombot_images\\video_button.png',
          'zoombot_images\\mute_button.png', 'zoombot_images\\more_options_button.png',
          'zoombot_images\\audio_settings_button.png', 'zoombot_images\\test_speaker_button.png',
          'zoombot_images\\line_1_button.png', 'zoombot_images\\exit_settings_button.png']

# Corresponding sleep times
sleep_times = [3, 5, 8, 8, 12, 12]

# Loop over each image
for image, sleep_time in zip(images, sleep_times):

    print(f"Processing image: {image}")
    # Read the template image
    template = cv2.imread(image, cv2.IMREAD_UNCHANGED)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    # Perform template matching at multiple scales
    scales = np.linspace(1.0, 0.2, 20)
    best_match = None
    best_scale = None
    best_confidence = -np.inf

    for scale in scales:
        resized_template = cv2.resize(template_gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        screenshot = np.array(pyautogui.screenshot())
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
        if image == 'zoombot_images\\browser_button.png':
            cv2.imwrite('screenshot_gray.png', screenshot_gray)

        match = cv2.matchTemplate(screenshot_gray, resized_template, cv2.TM_CCOEFF_NORMED)
        _, confidence, _, _ = cv2.minMaxLoc(match)

        if confidence > best_confidence:
            best_confidence = confidence
            best_match = match
            best_scale = scale

    _, _, _, best_loc = cv2.minMaxLoc(best_match)
    w, h = (template.shape[1] * best_scale, template.shape[0] * best_scale)
    x, y = (best_loc[0] + w / 2, best_loc[1] + h / 2)

    # If the confidence value does not reach the threshold
    if best_confidence < 0.4:
        print(f"{image} not found. Confidence: {best_confidence}")
    else:
        # Click on the found image
        pyautogui.click(x, y)
        print(f"{image} found. Confidence: {best_confidence}")

        # If the image is 'enter_name_button.png', type 'Bot' after clicking
        if image == 'zoombot_images\\enter_name_button.png':
            time.sleep(1)  # Wait for the text input field to activate
            pyautogui.write('Bot')  # Write 'Bot' using PyAutoGUI

    time.sleep(sleep_time)


    time.sleep(sleep_time)
