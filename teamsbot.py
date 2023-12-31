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

def join_teams_meeting(driver, meeting_link, audio_cable_image):
    if not meeting_link or not audio_cable_image:
        print("No Zoom link provided or Cable Image Provided. Exiting.")
        return

    print("Joining the meeting...")
    
    # Navigate to the meeting
    driver.get(meeting_link)
    
    time.sleep(7)  # wait for the page to load
    
    # List of images to find on the screen
    images = ['teamsbot_images\\browser_button.png',
              'teamsbot_images\\mute_button.png',
              'teamsbot_images\\enter_name_button.png',
              'teamsbot_images\\join_button.png',
              'teamsbot_images\\more_options_button.png',
              'teamsbot_images\\device_settings_button.png',
              'teamsbot_images\\speakers_list_button.png']
    
    # Corresponding sleep times
    sleep_times = [45, 2, 2, 25, 3, 2, 3,3]
    
    # Loop over each image
    for image, sleep_time in zip(images, sleep_times):

        # Press 'esc' key before looking for more_options_button
        if image == 'teamsbot_images\\more_options_button.png':
            pyautogui.press('esc')
            time.sleep(2)  # wait for the esc key effect to take place
    
        # Start a loop that continues until the image is found if the image is 'join_audio_button.png'
        while True:
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
    
                match = cv2.matchTemplate(screenshot_gray, resized_template, cv2.TM_CCOEFF_NORMED)
                _, confidence, _, _ = cv2.minMaxLoc(match)
    
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = match
                    best_scale = scale
    
            _, _, _, best_loc = cv2.minMaxLoc(best_match)
            w, h = (template.shape[1] * best_scale, template.shape[0] * best_scale)
            x, y = (best_loc[0] + w / 2, best_loc[1] + h / 2)
    
            # If the image is speakers_list_button , adjust the click position
            if image == 'teamsbot_images\\speakers_list_button.png':
                x, y = (best_loc[0] + w / 2, best_loc[1] + h)
                # x, y = (best_loc[0] + w, best_loc[1] + h // 2)
    
            # If the confidence value does not reach the threshold
            if (best_confidence < 0.4 and image != audio_cable_image) or \
               (image == audio_cable_image and best_confidence < 0.86):
                print(f"{image} not found. Confidence: {best_confidence}")
                if image == 'zoombot_images\\join_audio_button.png':
                    time.sleep(5)  # Wait for 5 seconds before searching again
                    continue
            else:
                # Click on the found image
                pyautogui.click(x, y)
    
                # If the image is 'enter_name_button.png', type 'Bot' after clicking
                if image == 'teamsbot_images\\enter_name_button.png':
                    time.sleep(1)  # Wait for the text input field to activate
                    pyautogui.write('Bot')  # Write 'Bot' using PyAutoGUI
    
            break  # Break out of the while loop if the image is found, or if it's not the 'join_audio_button.png'
    
        time.sleep(sleep_time)
    
    #Find this coordinate manually by hovering over the center of the dropdown menu and printing pyautogui.position()
    dropdown_menu_center = (1239, 679)  # Replace with the actual coordinates
    
    # Start a loop that continues until 'line_1_button_gray.png' is found
    while True:
        # Read the template image
        template = cv2.imread(audio_cable_image, cv2.IMREAD_UNCHANGED)
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
    
            match = cv2.matchTemplate(screenshot_gray, resized_template, cv2.TM_CCOEFF_NORMED)
            _, confidence, _, _ = cv2.minMaxLoc(match)
    
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = match
                best_scale = scale
    
        _, _, _, best_loc = cv2.minMaxLoc(best_match)
        w, h = (template.shape[1] * best_scale, template.shape[0] * best_scale)
        x, y = (best_loc[0] + w / 2, best_loc[1] + h / 2)
    
        # If 'line_1_button_gray.png' is not found, scroll down and continue
        if best_confidence < 0.86:  # Adjust this threshold as needed
            print(f"'Searching for available line button. Confidence: {best_confidence}")
            pyautogui.moveTo(dropdown_menu_center)  # Move to the dropdown menu
            pyautogui.scroll(-120)  # Adjust this value as needed
            time.sleep(1)  # Wait for a moment before the next check
            continue
        else:
            # If found, click on it and break the loop
            pyautogui.click(x, y)
            break
def check_end_of_teams_meeting():
    end_meeting_image = 'teamsbot_images\\meeting_ended_notification.png'  # Image of the notification that the meeting has ended
    confidence_threshold = 0.4  # Confidence threshold for template matching
    
    # Start the loop
    while True:
        # Take a screenshot
        screenshot = np.array(pyautogui.screenshot())
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    
        # Read the template image
        template = cv2.imread(end_meeting_image, cv2.IMREAD_UNCHANGED)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
        # Perform template matching at multiple scales
        scales = np.linspace(1.0, 0.2, 20)
        best_match = None
        best_scale = None
        best_confidence = -np.inf
    
        for scale in scales:
            resized_template = cv2.resize(template_gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    
            match = cv2.matchTemplate(screenshot_gray, resized_template, cv2.TM_CCOEFF_NORMED)
            _, confidence, _, _ = cv2.minMaxLoc(match)
    
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = match
                best_scale = scale
    
        # If the confidence value reaches the threshold, break the loop
        if best_confidence > confidence_threshold:
            print(f"End meeting notification found. Confidence: {best_confidence}")
            break
    
        # Sleep before the next check
        time.sleep(5)
