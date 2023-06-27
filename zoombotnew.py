import sys
import cv2
import numpy as np
import pyautogui
import time
import pygetwindow as gw
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

if len(sys.argv) > 1:
    meeting_link = sys.argv[1]
else:
    print("No Zoom link provided. Exiting.")
    sys.exit(1)
    
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--start-maximized")

chrome_options.add_experimental_option('prefs', {
  "protocol_handler": {
    "excluded_schemes": {
      "zoommtg": False
    }
  }
})

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get(meeting_link)

time.sleep(6) 

def locate_on_screen(image_path, confidence=0.8):
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    template = cv2.imread(image_path, 0)
    
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    match = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)

    if max_val < confidence:
        print(f"No match for '{image_path}' found on screen. Max match value is {max_val}.")
        return None

    return max_loc


def click_on_image(image_path, position='center'):
    loc = locate_on_screen(image_path)

    if loc is not None:
        img = cv2.imread(image_path)
        h, w, _ = img.shape

        if position == 'top-right':
            click_position = (loc[0] + w - 11, loc[1] + 10)
        elif position == 'bottom-center':
            click_position = (loc[0] + w // 2, loc[1] + h-10)
        elif position == 'right-center':
            click_position = (loc[0] + w, loc[1] + h // 2)
        else:
            click_position = (loc[0] + w // 2, loc[1] + h // 2)

        pyautogui.moveTo(click_position)
        pyautogui.click()
        return True
    else:
        print(f"Unable to locate image '{image_path}' on screen.")
        return False


def join_meeting(meeting_link): 
    time.sleep(7)
    if not click_on_image(r'zoombot_images\accept_cookies_button.png'):
        return

    click_on_image(r'zoombot_images\cookies_exit_button.png', 'top-right')
    click_on_image(r'zoombot_images\keep_button.png')
    
    time.sleep(4)

    click_on_image(r'zoombot_images\launch_meeting_button.png')
    
    time.sleep(5)

    click_on_image(r'zoombot_images\browser_button.png')
    
    start_time = time.time()

    while not click_on_image(r'zoombot_images\computer_audio_button.png') and time.time() - start_time < 120:
        time.sleep(5)

    if time.time() - start_time >= 120:
        print("Unable to join the meeting within time limit.")
        return

    click_on_image(r'zoombot_images\mute_button.png')
    print("Successfully joined the meeting.")
    
try:
    join_meeting(meeting_link)
except Exception as e:
    print("An error occurred while trying to join the meeting: ", e)
finally:
    time.sleep(5)
