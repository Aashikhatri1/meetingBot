from zoombot import create_browser_instance, join_meeting, check_end_of_meeting  
driver = create_browser_instance()
print('Joining the meeting...')
link = 'https://teams.live.com/meet/9512599422983'
available_cable = 'Line 1 (Virtual Audio Cable)'
join_meeting(driver, link, available_cable)



# import subprocess
# from pymongo import MongoClient
# import time
# from dotenv import load_dotenv
# import os
# import certifi
# from getCables import ServerHandler  # import ServerHandler from getCables.py
# from zoombot import create_browser_instance, join_meeting, check_end_of_meeting  # Import join_meeting and end_meeting_notification from zoombot.py
# ca = certifi.where()

# # Load environment variables from .env file
# load_dotenv()

# def check_new_submissions():
#     DB_CONNECTION = os.environ.get('DB_URI')
#     try:
#         client = MongoClient(DB_CONNECTION,tlsCAFile=ca)
#         Meeting_automation = client['Meeting_automation']
#         Zoom_meeting_link = Meeting_automation['Zoom_meeting_link']

#         last_count = Zoom_meeting_link.count_documents({})
#         print(f'Initial count: {last_count}')  # print initial count

#         while True:
#             current_count = Zoom_meeting_link.count_documents({})
#             print(f'Current count: {current_count}')  # print current count

#             if current_count > last_count:
#                 # fetch the latest document
#                 cursor = Zoom_meeting_link.find().sort([('_id', -1)]).limit(1)
#                 for doc in cursor:
#                     try:
#                         print(f'Document status: {doc["status"]}')  # Print the status regardless of its value

#                         # check if status is 'submitted'
#                         if doc['status'] == 'submitted':
#                             print(f'New document submitted: {doc}')
#                             link = doc['link']  # assuming 'link' is the field name for the meeting link
#                             print(f'Link: {link}')

#                             # Get the first available cable
#                             available_cable = ServerHandler.get_available_cable()
#                             print(f'First available cable: {available_cable}')

#                             # Change the status of the document to 'processing'
#                             result = Zoom_meeting_link.update_one({'_id': doc['_id']}, {"$set": {"status": "processing"}})

#                             # Print a success message if the update was successful
#                             if result.modified_count > 0:
#                                 print('Document status updated successfully.')
                                
#                                 # Run join_meeting with link as argument
#                                 driver = create_browser_instance()
#                                 print('Joining the meeting...')
#                                 join_meeting(driver, link, available_cable)
                                 

#                                 # Run recorder.py
#                                 print('Running recorder.py...')
#                                 recorder_process = subprocess.run(['python', 'recorder.py', str(doc['_id'])], capture_output=True)                                
#                                 if recorder_process.returncode == 0:
#                                     print('recorder.py finished successfully.')

#                                     # Get the path of the recorded audio from the stdout of recorder.py
#                                     recorded_file_path = recorder_process.stdout.decode().strip()

#                                     # Insert the path of the recorded audio into MongoDB
#                                     result = Zoom_meeting_link.update_one({'_id': doc['_id']}, {"$set": {"recordedFile": recorded_file_path}})
#                                     if result.modified_count > 0:
#                                         print(f'Inserted audio path into MongoDB: {recorded_file_path}')
#                                     else:
#                                         print('Failed to insert audio path into MongoDB.')
#                                      # Call end_meeting_notification to keep the meeting open unless it finds a notification on screen that the host has ended the meeting
#                                     check_end_of_meeting()  
                                   
#                                 else:
#                                     print('recorder.py failed.')
#                             else:
#                                 print('Failed to update document status.')
#                     except Exception as e:
#                         print(f'An error occurred while processing document: {e}')
#                 last_count = current_count
#             # wait for a while before checking again
#             time.sleep(3)  # adjust according to requirement
#     except Exception as e:
#         print(f'An error occurred: {e}')

# if __name__ == "__main__":
#     check_new_submissions()
