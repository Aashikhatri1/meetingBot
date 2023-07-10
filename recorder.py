import cv2
import numpy as np
import asyncio
import time
import sounddevice as sd
import soundfile as sf
import pyautogui
from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from getCables import ServerHandler
import os
import sys
import certifi
ca = certifi.where()

# Load environment variables from .env file
load_dotenv()

FS = 44100
BUFFER = []
CHECK_FREQUENCY = 5  # seconds
# TEMPLATE_PATH = r'zoombot_images\meeting_ended_notification.png'
TEMPLATE_PATH_ZOOM = r'zoombot_images\meeting_ended_notification.png'
#TEMPLATE_PATH_MEET = r'meetbot_images\meeting_ended_notification.png'
TEMPLATE_PATH_TEAMS = r'teamsbot_images\meeting_ended_notification.png'
DB_CONNECTION = os.environ.get('DB_URI')

class Recorder:
    def __init__(self, link_id, device_name):
        self.device_name = device_name
        self.device_id = None
        self.recording = False
        self.link_id = link_id
        self.stream = None
        self.client = MongoClient(DB_CONNECTION,tlsCAFile=ca)
        self.db = self.client["Meeting_automation"]
        self.col_links = self.db["Zoom_meeting_link"]

    def callback(self, indata, frames, time, status):
        if self.recording:
            BUFFER.extend(indata[:, 0])  # Assuming mono recording
          
    def get_link(self):
        link_doc = self.col_links.find_one({"_id": ObjectId(self.link_id)})
        return link_doc['link'] if link_doc else None

    # link = Recorder.get_link()
    available_cable_name = ServerHandler.get_available_cable_name()

    @staticmethod
    def get_device_id_for_cable(available_cable_name):
            device_info = sd.query_devices()
            for i, device in enumerate(device_info):
                if device['name'] == available_cable_name:
                    return i
            raise ValueError(f"No device found with name: {available_cable_name}")

    async def start_recording(self):
        print(f"Starting recording")
        
        self.device_id = self.get_device_id_for_cable(self.device_name)
        self.stream = sd.InputStream(samplerate=FS, channels=1, device=self.device_id, callback=self.callback)
        self.recording = True
        self.stream.start()

        # Update Meeting_link collection
        try:
            self.col_links.update_one({"_id": ObjectId(self.link_id)}, {"$set": {"status": "recording"}})
            print(f'Recording on {self.device_name}') 
        except PyMongoError as e:
            print(f"Error occurred while updating the start recording status: {e}")

    async def stop_recording(self):
        print("Stopping recording")
        self.stream.stop()
        self.recording = False
        self.save_recording()

        # Update Meeting_link collection
        try:
            self.col_links.update_one({"_id": ObjectId(self.link_id)}, {"$set": {"status": "Recording Completed", "recordedFile": "recording.wav"}})
        except PyMongoError as e:
            print(f"Error occurred while updating the stop recording status: {e}")

    def save_recording(self):
        sf.write('recording.wav', np.array(BUFFER), FS)

    # async def check_screen(self, link):
    # async def check_screen(self):
    #     link = self.get_link()
        
    #     if 'zoom' in link.lower():
    #         template = cv2.imread(TEMPLATE_PATH_ZOOM, cv2.IMREAD_GRAYSCALE)
    #     elif 'teams' in link.lower():
    #         template = cv2.imread(TEMPLATE_PATH_TEAMS, cv2.IMREAD_GRAYSCALE)

    #     while True:
    #         await asyncio.sleep(CHECK_FREQUENCY)
    #         if not self.recording:
    #             return
    #         screenshot = pyautogui.screenshot()
    #         screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    #         screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    #         res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    #         cv2.imwrite('end_ss.png', screenshot_gray)
    #         threshold = 0.5
    #         loc = np.where(res >= threshold)
            
    #         # Log max_val for debugging
    #         min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    #         print(f"Max match value: {max_val}")
            
    #         if len(loc[0]) > 0:
    #             print("Match found, stopping recording.")
    #             await self.stop_recording()
    #         else:
    #             print("Match not found.")

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
                await self.stop_recording()
                break

async def main():
    link_id = sys.argv[1]
    device_name = sys.argv[2]  # New argument for the device name
    recorder = Recorder(link_id, device_name)
    await recorder.start_recording()
    # asyncio.create_task(recorder.check_screen(link))
    # asyncio.create_task(recorder.check_screen())
    asyncio.create_task(recorder.check_end_of_teams_meeting())
    await asyncio.sleep(35)
    if recorder.recording:
        await recorder.stop_recording()

asyncio.run(main())
