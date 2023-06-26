
import subprocess
from pymongo import MongoClient
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def check_new_submissions():
    try:
        client = MongoClient(os.environ.get('DB_URI'))
        Meeting_automation = client['Meeting_automation']
        Zoom_meeting_link = Meeting_automation['Zoom_meeting_link']

        last_count = Zoom_meeting_link.count_documents({})
        print(f'Initial count: {last_count}')  # print initial count

        while True:
            current_count = Zoom_meeting_link.count_documents({})
            print(f'Current count: {current_count}')  # print current count

            if current_count > last_count:
                # fetch the latest document
                cursor = Zoom_meeting_link.find().sort([('_id', -1)]).limit(1)
                for doc in cursor:
                    try:
                        print(f'Document status: {doc["status"]}')  # Print the status regardless of its value

                        # check if status is 'submitted'
                        if doc['status'] == 'submitted':
                            print(f'New document submitted: {doc}')
                            link = doc['link']  # assuming 'link' is the field name for the meeting link
                            print(f'Link: {link}')

                            # Change the status of the document to 'processing'
                            result = Zoom_meeting_link.update_one({'_id': doc['_id']}, {"$set": {"status": "processing"}})

                            # Print a success message if the update was successful
                            if result.modified_count > 0:
                                print('Document status updated successfully.')
                                
                                # Run zoombot.py with link as argument
                                print('Running zoombot.py...')
                                subprocess.run(['python', r'zoombot.py', link])  # replace with the path to your zoom bot file

                                # Run recorder.py
                                print('Running recorder.py...')
                                recorder_process = subprocess.run(['python', r'recorder.py'], capture_output=True,args=str(doc['_id']))  # replace with the path to your recorder file
                                
                                if recorder_process.returncode == 0:
                                    print('recorder.py finished successfully.')

                                    # Get the path of the recorded audio from the stdout of recorder.py
                                    recorded_file_path = recorder_process.stdout.decode().strip()

                                    # Insert the path of the recorded audio into MongoDB
                                    result = Zoom_meeting_link.update_one({'_id': doc['_id']}, {"$set": {"recordedFile": recorded_file_path}})
                                    if result.modified_count > 0:
                                        print(f'Inserted audio path into MongoDB: {recorded_file_path}')
                                    else:
                                        print('Failed to insert audio path into MongoDB.')
                                else:
                                    print('recorder.py failed.')

                            else:
                                print('Failed to update document status.')
                    except Exception as e:
                        print(f'An error occurred while processing document: {e}')
                last_count = current_count
            # wait for a while before checking again
            time.sleep(3)  # adjust according to requirement
    except Exception as e:
        print(f'An error occurred: {e}')
# sample commit
if __name__ == "__main__":
    check_new_submissions()

