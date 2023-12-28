import subprocess
from pymongo import MongoClient
import time
from dotenv import load_dotenv
import os
import certifi
from bson import ObjectId
import boto3
import requests
import time

ca = certifi.where()
from API_requests import send_post_request, get_diarisation_result, get_all_indicator_list, create_indicator_diarisation, save_diarisation_to_file, upload_file_to_s3
from analysis import gpt_response

# Load environment variables from .env file
load_dotenv()

def check_for_recording_url():

    DB_CONNECTION = os.environ.get('DB_URI')
    ca = certifi.where()

    try:
        client = MongoClient(DB_CONNECTION, tlsCAFile=ca)
        Meeting_automation = client['Meeting_automation']
        recording_link = Meeting_automation['recordingLink']

        last_count = recording_link.count_documents({})
        print(f'Initial count: {last_count}')

        while True:
            current_count = recording_link.count_documents({})
            print(f'Current count: {current_count}')

            if current_count > last_count:
                cursor = recording_link.find().sort([('_id', -1)]).limit(1)
                documents = list(cursor)  # Convert cursor to list
                if len(documents) > 0:
                    latest_document = documents[0]
                    id = latest_document["id"]  # Extracting the ID
                    rtype = latest_document["type"] 
                    print(f"Received new submission with ID: {id}")
                    # You can now use 'id' as needed
                    time.sleep(1*60)
                    diarisation = get_diarisation_result(id)
                    print('diarisation', diarisation)

                    #upload_diarisation = create_meeting_diarisation(str(id), diarisation)
                    #print('upload_diarisation', upload_diarisation)
                    
                    saved_diarisation = save_diarisation_to_file(id)
                    upload_to_s3 = upload_file_to_s3(id, object_name=None)
                    print('upload_to_s3', upload_to_s3)

                    indicators = get_all_indicator_list()
                    print('indicators', indicators)

                    recording_analysis = gpt_response(indicators, diarisation)
                    print('recording_analysis', recording_analysis)

                    upload_analysis = create_indicator_diarisation(str(id), rtype, diarisation, recording_analysis)
                    print('upload_analysis',upload_analysis) 
                        
                    
                    last_count = current_count

            # Sleep for some time before next check
            time.sleep(3)  # adjust the sleep time as per your requirements

    except Exception as e:
        print(f"An error occurred: {e}")
        

if __name__ == "__main__":
    check_for_recording_url()