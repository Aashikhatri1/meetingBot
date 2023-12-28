# Sending recording for Diarisation ( Hitting API)

import requests
import json
import boto3
from dotenv import load_dotenv
import os
from botocore.exceptions import NoCredentialsError
load_dotenv()

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

def send_post_request(file_path, id):

    url = 'https://three65analytics-jtgo.onrender.com/upload'
    # Prepare the files and data for the POST request
    files = {'file': (file_path, open(file_path, 'rb'))}
    data = {'id': id}

    # Send the POST request
    response = requests.post(url, files=files, data=data)

    return response

def get_diarisation_result(task_id):
    # URL of the result endpoint
    url = f"https://three65analytics-jtgo.onrender.com/result/{task_id}"

    try:
        response = requests.get(url)
        response = response.json()
        diarisation_content = response.get('result', {}) if isinstance(response, dict) else response
        
        # Return the server's response as a Python dictionary
        return diarisation_content
    except requests.RequestException as e:
        # Handle any errors that occur during the request
        return {'error': str(e)}

def save_diarisation_to_file(task_id):
    file_name = f"{task_id}.txt"
    diarisation = get_diarisation_result(task_id)
    with open(file_name, 'w') as file:
        file.write(str(diarisation))


def upload_file_to_s3(task_id, object_name=None):
    bucket = S3_BUCKET_NAME
    file_name = f"{task_id}.txt"
    if object_name is None:
        object_name = file_name
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except NoCredentialsError as e:
        print("Credentials not available:", e)
        return False
    except Exception as e:
        print("An error occurred:", e)
        return False
    return True

def get_all_indicator_list():
    url = "https://salescrmbe.onrender.com/api/indicator/find-all"

    try:
        response = requests.get(url)
        return response.json()
    except requests.RequestException as e:
        return {'error': str(e)}

def create_indicator_diarisation(id, rtype, diarisation, analysis):
    url = "https://salescrmbe.onrender.com/api/create-diarisation"
    headers = {'Content-Type': 'application/json'}

    # Extracting the diarisation string
    diarisation_string = next(iter(diarisation.values())) if isinstance(diarisation, dict) else diarisation
    print(diarisation_string)
    # Splitting the transcript into lines and processing each line
    diarisation_list = []
    lines = diarisation_string.split("\n")
    for i in range(0, len(lines), 2):
        if i+1 < len(lines):
            speaker = lines[i].strip()
            text = lines[i+1].strip()
            diarisation_list.append({speaker: text})
    # Extract the JSON part from the analysis string
    json_start = analysis.find('{')
    json_end = analysis.rfind('}') + 1  # +1 to include the closing brace
    json_part = analysis[json_start:json_end]

    # Parse the JSON string
    try:
        analysis_json = json.loads(json_part)
    except json.JSONDecodeError as e:
        print("Error decoding JSON string:", e)
        analysis_json = {}

    # Construct the payload
    payload = {
        "id": id,
        "type": rtype,
        "data": {
            "diarisation": diarisation_list,  # diarisation maps to a string
            "analysis": [analysis_json] # Second element of the array
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()
    except requests.RequestException as e:
        return {'error': str(e)}

