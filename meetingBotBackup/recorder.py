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
template_path_zoom = r'zoombot_images\meeting_ended_notification.png'
template_path_teams = r'teamsbot_images\meeting_ended_notification.png'

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
    async def check_screen(self):

        link = self.get_link()
        
        if 'zoom' in link.lower():
            template_path = template_path_zoom
        elif 'teams' in link.lower():
            template_path = template_path_teams
        
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        scales = np.linspace(1.0, 0.2, 20)
        threshold = 0.5  # Confidence threshold for template matching

        while True:
            await asyncio.sleep(CHECK_FREQUENCY)
            if not self.recording:
                return

            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

            best_match = None
            best_scale = None
            best_confidence = -np.inf

            for scale in scales:
                resized_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

                match = cv2.matchTemplate(screenshot_gray, resized_template, cv2.TM_CCOEFF_NORMED)
                _, confidence, _, _ = cv2.minMaxLoc(match)

                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = match
                    best_scale = scale

            if best_confidence > threshold:
                print(f"End meeting notification found. Confidence: {best_confidence}")
                await self.stop_recording()

async def main():
    link_id = sys.argv[1]
    device_name = sys.argv[2]  # New argument for the device name
    recorder = Recorder(link_id, device_name)
    await recorder.start_recording()
    # asyncio.create_task(recorder.check_screen(link))
    asyncio.create_task(recorder.check_screen())
    await asyncio.sleep(35)
    if recorder.recording:
        await recorder.stop_recording()

asyncio.run(main())


# import cv2
# import numpy as np
# import asyncio
# import time
# import sounddevice as sd
# import soundfile as sf
# import pyautogui
# from pymongo import MongoClient
# from dotenv import load_dotenv
# from pymongo.errors import PyMongoError
# from bson.objectid import ObjectId
# from getCables import ServerHandler
# import os
# import sys
# import certifi
# ca = certifi.where()

# # Load environment variables from .env file
# load_dotenv()

# FS = 44100
# BUFFER = []
# CHECK_FREQUENCY = 5  # seconds
# template_path_zoom = r'zoombot_images\meeting_ended_notification.png'
# template_path_teams = r'teamsbot_images\meeting_ended_notification.png'

# DB_CONNECTION = os.environ.get('DB_URI')

# class Recorder:
#     def __init__(self, link_id, device_name):
#         self.device_name = device_name
#         self.device_id = None
#         self.recording = False
#         self.link_id = link_id
#         self.stream = None
#         self.client = MongoClient(DB_CONNECTION,tlsCAFile=ca)
#         self.db = self.client["Meeting_automation"]
#         self.col_links = self.db["Zoom_meeting_link"]

#     def callback(self, indata, frames, time, status):
#         if self.recording:
#             BUFFER.extend(indata[:, 0])  # Assuming mono recording

#     available_cable_name = ServerHandler.get_available_cable_name()

#     @staticmethod
#     def get_device_id_for_cable(available_cable_name):
#             device_info = sd.query_devices()
#             for i, device in enumerate(device_info):
#                 if device['name'] == available_cable_name:
#                     return i
#             raise ValueError(f"No device found with name: {available_cable_name}")

#     async def start_recording(self):
#         print(f"Starting recording")
        
#         self.device_id = self.get_device_id_for_cable(self.device_name)
#         self.stream = sd.InputStream(samplerate=FS, channels=1, device=self.device_id, callback=self.callback)
#         self.recording = True
#         self.stream.start()

#         # Update Meeting_link collection
#         try:
#             self.col_links.update_one({"_id": ObjectId(self.link_id)}, {"$set": {"status": "recording"}})
#             print(f'Recording on {self.device_name}') 
#         except PyMongoError as e:
#             print(f"Error occurred while updating the start recording status: {e}")

#     async def stop_recording(self):
#         print("Stopping recording")
#         self.stream.stop()
#         self.recording = False
#         self.save_recording()

#         # Update Meeting_link collection
#         try:
#             self.col_links.update_one({"_id": ObjectId(self.link_id)}, {"$set": {"status": "Recording Completed", "recordedFile": "recording.wav"}})
#         except PyMongoError as e:
#             print(f"Error occurred while updating the stop recording status: {e}")

#     def save_recording(self):
#         sf.write('recording.wav', np.array(BUFFER), FS)

#     # async def check_screen(self, link):
#     async def check_screen(self):

#         link = self.get_link()
        
#         if 'zoom' in link.lower():
#             template_path = template_path_zoom
#         elif 'teams' in link.lower():
#             template_path = template_path_teams
        
#         template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
#         scales = np.linspace(1.0, 0.2, 20)
#         threshold = 0.5  # Confidence threshold for template matching

#         while True:
#             await asyncio.sleep(CHECK_FREQUENCY)
#             if not self.recording:
#                 return

#             screenshot = pyautogui.screenshot()
#             screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
#             screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

#             best_match = None
#             best_scale = None
#             best_confidence = -np.inf

#             for scale in scales:
#                 resized_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

#                 match = cv2.matchTemplate(screenshot_gray, resized_template, cv2.TM_CCOEFF_NORMED)
#                 _, confidence, _, _ = cv2.minMaxLoc(match)

#                 if confidence > best_confidence:
#                     best_confidence = confidence
#                     best_match = match
#                     best_scale = scale

#             if best_confidence > threshold:
#                 print(f"End meeting notification found. Confidence: {best_confidence}")
#                 await self.stop_recording()

# async def main():
#     link_id = sys.argv[1]
#     device_name = sys.argv[2]  # New argument for the device name
#     recorder = Recorder(link_id, device_name)
#     await recorder.start_recording()
#     # asyncio.create_task(recorder.check_screen(link))
#     asyncio.create_task(recorder.check_screen())
#     await asyncio.sleep(35)
#     if recorder.recording:
#         await recorder.stop_recording()

# asyncio.run(main())

