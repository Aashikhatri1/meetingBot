# meet audio recording code
import pyautogui
import cv2
import numpy as np
import time
import webbrowser

#This function will find the image on the screen and return its position
def locate_on_screen(image_path, confidence=0.8):
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

# The main function to join a meeting
def join_google_meeting(driver, link, available_cable):
    def open_website(url):
        webbrowser.open(url, new=2)  # new=2 opens in a new tab, if possible

    # Opening call hipppo dialer
    # website = 'https://meet.google.com/uis-agfm-usq'
    open_website(link)

    time.sleep(10)  # wait for the page to load

    # # Click on the camera button
    # if not click_on_image(r'C:\Users\LENOVO\anaconda3\camera_button.png'):
    #     print("Couldn't find the camera button")
    #     return
    
    # Click on the microphone button
    if not click_on_image(r'meetbot_images\microphone_button.png'):
        print("Couldn't find the microphone button")
        return
    
    click_on_image(r'meetbot_images\name_button.png')
    pyautogui.write('Balpreet Singh')
        
    # Click on the "Ask to join" button
    if not click_on_image(r'meetbot_images\ask_to_join_button.png'):
        print("Couldn't find the 'Ask to join' button")
        # Now, try to click on "Join now" button
        if not click_on_image(r'meetbot_images\join_now_button.png'):
            print("Couldn't find the 'Join now' button either")
            return

    print("Successfully joined the meeting")

    time.sleep(20)

    # Click on the "More options" button
    #if not click_on_image(r'meetbot_images\more_options_button.png'):
        #print("Couldn't find the 'More options' button")
        #return
    
    #time.sleep(2)
    
    #if not click_on_image(r'meetbot_images\settings_button.png'):
        #print("Couldn't find the 'Settings' button")
        #return
    
    #time.sleep(3)
    
    #if not click_on_image(r'meetbot_images\speakers_button.png'):
        #print("Couldn't find the 'Speakers' button")
        #return
    
    #time.sleep(2)

    #if not click_on_image(r'meetbot_images\line_1_button.png'):
        #print("Couldn't find the 'Line 1' button")
        #return
    
    #time.sleep(2)
    
    #if not click_on_image(r'meetbot_images\exit_settings_button.png'):
        #print("Couldn't find the 'Exit Settings' button")
        #return
#link = 'https://meet.google.com/uis-agfm-usq'    
# Call the function with your meeting link
#join_meeting('abc', link, 'line1')
