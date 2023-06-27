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
from screeninfo import get_monitors
import ctypes
meeting_link = 'https://us04web.zoom.us/j/2349397688?pwd=SWRGSElROXlwc2xQdG93REFDdm1iUT09'

def change_screen_resolution(width, height):
    user32 = ctypes.windll.user32
    user32.ChangeDisplaySettingsW(None, 0)
    DM_BITSPERPEL = 0x00040000
    DM_PELSWIDTH = 0x00080000
    DM_PELSHEIGHT = 0x00100000
    DM_SIZE = 0x001C0000

    mode = user32.DEVMODEW()
    mode.dmSize = ctypes.sizeof(user32.DEVMODEW)
    mode.dmPelsWidth = width
    mode.dmPelsHeight = height
    mode.dmBitsPerPel = 32
    mode.dmFields = DM_BITSPERPEL | DM_PELSWIDTH | DM_PELSHEIGHT

    if user32.ChangeDisplaySettingsW(ctypes.byref(mode), 0) != 0:
        raise Exception("Failed to change screen resolution")

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
    
def main():
    original_resolution = get_monitors()[0]
    desired_resolution = (1920, 1080)
    try:
        change_screen_resolution(*desired_resolution)
        if len(sys.argv) > 1:
            meeting_link = sys.argv[1]
        else:
            print("No Zoom link provided. Exiting.")
            return
        join_meeting(meeting_link)
    finally:
        change_screen_resolution(original_resolution.width, original_resolution.height)

if __name__ == "__main__":
    main()
