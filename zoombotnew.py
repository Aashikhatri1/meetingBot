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
from PIL import ImageChops, Image
import io
import urllib

# Function to compare images
def image_diff(img1, img2):
    diff = ImageChops.difference(img1, img2)
    return np.sum(np.array(diff))

def compare_images(image_path):
    template = Image.open(image_path)
    screenshot = Image.open(io.BytesIO(pyautogui.screenshot().tobytes()))
    best_confidence = np.inf
    best_loc = None

    for i in range(screenshot.width - template.width):
        for j in range(screenshot.height - template.height):
            box = (i, j, i + template.width, j + template.height)
            screenshot_piece = screenshot.crop(box)
            confidence = image_diff(template, screenshot_piece)
            if confidence < best_confidence:
                best_confidence = confidence
                best_loc = (i + template.width / 2, j + template.height / 2)

    return best_confidence, best_loc

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
          'zoombot_images\\keep_button.png',
          'zoombot_images\\launch_meeting_button.png', 'zoombot_images\\browser_button.png',
          'zoombot_images\\agree_button.png', 'zoombot_images\\enter_name_button.png',
          'zoombot_images\\join_button.png', 'zoombot_images\\video_button1.png',
          'zoombot_images\\mute_button1.png', 'zoombot_images\\more_options_button.png',
          'zoombot_images\\audio_settings_button1.png', 'zoombot_images\\test_speaker_button1.png',
          'zoombot_images\\line_1_button1.png', 'zoombot_images\\exit_settings_button1.png',
          'zoombot_images\\maximize_button.png', 'zoombot_images\\video_button.png',
          'zoombot_images\\mute_button.png', 'zoombot_images\\more_options_button.png',
          'zoombot_images\\audio_settings_button.png', 'zoombot_images\\test_speaker_button.png',
          'zoombot_images\\line_1_button.png', 'zoombot_images\\exit_settings_button.png']

# Sleep times for each image
sleep_times = [3, 5, 3, 5, 5, 5]

# Loop over each image
for i, image in enumerate(images):
    confidence, location = compare_images(image)
    if confidence == 0:
        # Image found, click on it
        pyautogui.click(location)
        print(f"{image} clicked")
    else:
        print(f"{image} not found")
    # Sleep for the specified amount of time
    if i < len(sleep_times):
        time.sleep(sleep_times[i])
    else:
        time.sleep(1)
