meeting_link = 'https://meet.google.com/nun-sbbq-smo' 

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import cv2
import numpy as np
import pyautogui
import time
import subprocess
import pygetwindow as gw
from selenium.webdriver.common.keys import Keys
import os
import shutil
from teamsbot import join_meeting, check_end_of_meeting  

# This function creates a new Chrome profile
def create_new_profile_directory():
    # Specify the base directory for the profiles
    base_dir = r"C:\Users\LENOVO\anaconda3\chrome_profiles"

    # Create a new directory for the new profile
    profile_dir = os.path.join(base_dir, "profile_" + str(time.time()).replace(".", "_"))
    os.makedirs(profile_dir, exist_ok=True)

    return profile_dir

# This function will delete the profile directory
def delete_profile_directory(profile_dir):
    shutil.rmtree(profile_dir)

def create_browser_instance():
    # Create a new profile
    profile_dir = create_new_profile_directory()

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Disable popup for allowing webcam and microphone
    chrome_options.add_argument("--disable-notifications")  # Disable notifications
    chrome_options.add_argument("--start-maximized")  # Open browser in maximized mode
    chrome_options.add_argument(f"user-data-dir={profile_dir}")  # Use a new profile
    chrome_options.add_experimental_option('prefs', {
        "protocol_handler": {
            "excluded_schemes": {
                "zoommtg": False
            }
        }
    })

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    return driver, profile_dir


driver, profile_dir = create_browser_instance()
print('Joining the meeting...')
available_cable = 'Line 1 (Virtual Audio Cable)'
join_meeting(driver, meeting_link, available_cable)





# # This function will start the browser
# def start_browser():
#     # Command to start Chrome
#     cmd = "start chrome --remote-debugging-port=9222"
    
#     # Run the command in a new shell
#     subprocess.Popen(cmd, shell=True)

#     time.sleep(5)  # wait for the browser to open

# # This function will bring the browser to front
# def bring_browser_to_front():
#     # Get a list of all open windows
#     windows = gw.getAllWindows()

#     # Find the browser window and bring it to the front
#     for window in windows:
#         if "chrome" in window.title.lower():
#             window.activate()

# # Call the function to start the browser
# start_browser()

# # This function will find the image on the screen and return its position
# def locate_on_screen(image_path, confidence=0.8):
#     # capture the screen
#     screenshot = pyautogui.screenshot()
#     screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

#     # read the image file
#     template = cv2.imread(image_path, 0)
    
#     # convert the screenshot to grayscale
#     gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

#     # match the template with the screenshot
#     match = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)

#     # if the match is not good enough return None
#     if max_val < confidence:
#         return None

#     return max_loc

# # This function will click on the center of an image on the screen
# def click_on_image(image_path):
#     loc = locate_on_screen(image_path)

#     if loc is not None:
#         # get the size of the image
#         img = cv2.imread(image_path)
#         h, w, _ = img.shape

#         # calculate the center of the image
#         center = (loc[0] + w // 2, loc[1] + h // 2)

#         # move the cursor to the center of the image and click
#         pyautogui.moveTo(center)
#         pyautogui.click()
#         return True
#     else:
#         return False

# # The main function to join a meeting
# def join_meeting(meeting_link):
#     # Open the browser
#     # Set up Chrome options
#     chrome_options = Options()
#     chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Disable popup for allowing webcam and microphone
#     chrome_options.add_argument("--disable-notifications")  # Disable notifications
#     chrome_options.add_argument("--start-maximized")  # Open browser in maximized mode

#     # Add Chrome debugging option
#     chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#     # Navigate to the meeting
#     driver.get(meeting_link)

#     bring_browser_to_front()

#     time.sleep(10)  # wait for the page to load

#     # Click on the camera button
#     if not click_on_image(r'C:\Users\LENOVO\anaconda3\camera_button.png'):
#         print("Couldn't find the camera button")
#         return
    
#     # Click on the microphone button
#     if not click_on_image(r'C:\Users\LENOVO\anaconda3\microphone_button.png'):
#         print("Couldn't find the microphone button")
#         return

#     # Click on the "Ask to join" button
#     if not click_on_image(r'C:\Users\LENOVO\anaconda3\ask_to_join_button.png'):
#         print("Couldn't find the 'Ask to join' button")
#         # Now, try to click on "Join now" button
#         if not click_on_image(r'C:\Users\LENOVO\anaconda3\join_now_button.png'):
#             print("Couldn't find the 'Join now' button either")
#             return

#     print("Successfully joined the meeting")

#     time.sleep(20)

#     # Click on the "More options" button
#     if not click_on_image(r'C:\Users\LENOVO\anaconda3\more_options_button.png'):
#         print("Couldn't find the 'More options' button")
#         return
    
#     time.sleep(2)
    
#     if not click_on_image(r'C:\Users\LENOVO\anaconda3\settings_button.png'):
#         print("Couldn't find the 'Settings' button")
#         return
    
#     time.sleep(3)
    
#     if not click_on_image(r'C:\Users\LENOVO\anaconda3\speakers_button.png'):
#         print("Couldn't find the 'Speakers' button")
#         return
    
#     time.sleep(2)

#     if not click_on_image(r'C:\Users\LENOVO\anaconda3\line_1_button.png'):
#         print("Couldn't find the 'Line 1' button")
#         return
    
#     time.sleep(2)
    
#     if not click_on_image(r'C:\Users\LENOVO\anaconda3\exit_settings_button.png'):
#         print("Couldn't find the 'Exit Settings' button")
#         return
    
# # Call the function with your meeting link
# join_meeting(meeting_link)
