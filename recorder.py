import cv2
import numpy as np
import asyncio
import time
import sounddevice as sd
import soundfile as sf
import pyautogui
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import sys
import certifi
ca = certifi.where()

# Load environment variables from .env file
load_dotenv()

FS = 44100
BUFFER = []
CHECK_FREQUENCY = 5  # seconds
TEMPLATE_PATH = r'zoombot_images\meeting_ended_notification.png'
DB_CONNECTION = os.environ.get('DB_URI')

class Recorder:
    def __init__(self, link_id):
        self.device_name = None
        self.device_id = None
        self.recording = False
        self.link_id = link_id
        self.stream = None
        self.client = MongoClient(DB_CONNECTION,tlsCAFile=ca)
        self.db = self.client["Meeting_automation"]
        self.col_cables = self.db["serverCables"]
        self.col_links = self.db["Zoom_meeting_link"]
        
    def callback(self, indata, frames, time, status):
        if self.recording:
            BUFFER.extend(indata[:, 0])  # Assuming mono recording

    async def start_recording(self):
        print(f"Starting recording")

        document = self.col_cables.find_one({"name": "Server 1"})  # Get document by server name
        if document:
            if len(document['availableCables']) == 0:
                print("No cables available for recording, try again later.")
                raise Exception("No cables available for recording")
            self.device_name = document['availableCables'].pop(0)
            document['busyCables'].append(self.device_name)
            self.col_cables.update_one({"_id": document["_id"]}, {"$set": {"availableCables": document['availableCables'], "busyCables": document['busyCables']}})
            # Update Meeting_link collection
            self.col_links.update_one({"_id": self.link_id}, {"$set": {"status": "recording"}})
            print(f'Recording on {self.device_name}') 

        device_info = sd.query_devices()
        for i, device in enumerate(device_info):
            if device['name'] == self.device_name:
                self.device_id = i
                break

        if self.device_id is None:
            raise ValueError(f"No device found with name: {self.device_name}")

        self.stream = sd.InputStream(samplerate=FS, channels=1, device=self.device_id, callback=self.callback)
        self.recording = True
        self.stream.start()

    async def stop_recording(self):
        print("Stopping recording")
        self.stream.stop()
        self.recording = False
        self.save_recording()

        document = self.col_cables.find_one({"name": "Server 1"})  # Get document by server name
        if document:
            if self.device_name in document['busyCables']:
                document['busyCables'].remove(self.device_name)
                document['availableCables'].insert(0, self.device_name)
                self.col_cables.update_one({"_id": document["_id"]}, {"$set": {"availableCables": document['availableCables'], "busyCables": document['busyCables']}})

        # Update Meeting_link collection
        self.col_links.update_one({"_id": self.link_id}, {"$set": {"status": "Recording Completed", "recordedFile": "recording.wav"}})

    def save_recording(self):
        sf.write('recording.wav', np.array(BUFFER), FS)

    async def check_screen(self):
        template = cv2.imread(TEMPLATE_PATH, cv2.IMREAD_GRAYSCALE)
        while True:
            await asyncio.sleep(CHECK_FREQUENCY)
            if not self.recording:
                return
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)
            if len(loc[0]) > 0:
                await self.stop_recording()

async def main():
    link_id = int(sys.argv[1])  # Convert input argument to integer
    recorder = Recorder(link_id)  
    await recorder.start_recording()
    asyncio.create_task(recorder.check_screen())
    await asyncio.sleep(25)
    if recorder.recording:
        await recorder.stop_recording()

asyncio.run(main())
