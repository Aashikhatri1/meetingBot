import time
from API_requests import send_post_request, get_diarisation_result, create_meeting_diarisation, get_all_indicator_list, create_indicator_diarisation, save_diarisation_to_file, upload_file_to_s3
from analysis import gpt_response

from dotenv import load_dotenv
import os
load_dotenv()
from bson import ObjectId
file_path = 'recording.wav'
id = "6585ca49f77bb95d805f8822"
id= ObjectId(id)
response = send_post_request(file_path, id)
print('response', response.text)   

#time.sleep(5*60)
time.sleep(2*60)
diarisation = get_diarisation_result(id)
print('diarisation', diarisation)


upload_diarisation = create_meeting_diarisation(str(id), diarisation)
print('upload_diarisation', upload_diarisation)

saved_diarisation = save_diarisation_to_file(id)
upload_to_s3 = upload_file_to_s3(id, object_name=None)
print('upload_to_s3', upload_to_s3)

indicators = get_all_indicator_list()
print('indicators', indicators)

recording_analysis = gpt_response(indicators, diarisation)
print('recording_analysis', recording_analysis)

upload_analysis = create_indicator_diarisation(str(id), recording_analysis)
print('upload_analysis',upload_analysis)