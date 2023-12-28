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
    #url = 'https://diarisation.onrender.com/upload'   # Url for post request to send audio.wav
    # Prepare the files and data for the POST request
    files = {'file': (file_path, open(file_path, 'rb'))}
    data = {'id': id}

    # Send the POST request
    response = requests.post(url, files=files, data=data)

    return response

def get_diarisation_result(task_id):
    # URL of the result endpoint
    #url = f"https://diarisation.onrender.com/result/{task_id}"
    url = f"https://three65analytics-jtgo.onrender.com/result/{task_id}"

    try:
        response = requests.get(url)
        response = response.json()
        diarisation_content = response.get('result', {}) if isinstance(response, dict) else response
        #diarisation_content = diarisation.get('result', {}) if isinstance(diarisation, dict) else diarisation
        # Return the server's response as a Python dictionary
        #return response.json()
        return diarisation_content
    except requests.RequestException as e:
        # Handle any errors that occur during the request
        return {'error': str(e)}

def save_diarisation_to_file(task_id):
    file_name = f"{task_id}.txt"
    diarisation = get_diarisation_result(task_id)
    with open(file_name, 'w') as file:
        file.write(str(diarisation))

def upload_file_to_s3_old(task_id, object_name=None):
    bucket= S3_BUCKET_NAME
    file_name = f"{task_id}.txt"
    if object_name is None:
        object_name = file_name
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except NoCredentialsError:
        print("Credentials not available")
        return False
    return True

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


def create_meeting_diarisation(id, diarisation):
    url = "https://salescrmbe.onrender.com/api/create-diarisation"  # Replace with your actual endpoint URL
    headers = {'Content-Type': 'application/json'}
    
    # Construct the payload
    payload = {
        "id": id,
        "type": 'meeting',
        "data": diarisation
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()
    except requests.RequestException as e:
        return {'error': str(e)}


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

def create_indicator_diarisation3(id, rtype, diarisation, analysis):
    url = "https://salescrmbe.onrender.com/api/create-diarisation"
    headers = {'Content-Type': 'application/json'}

    # Extracting the diarisation string
    diarisation_string = next(iter(diarisation.values())) if isinstance(diarisation, dict) else diarisation
    lines = diarisation_string.strip().split("\n")

    # Process each line and structure it into a dictionary
    diarisation_data = {}
    for line in lines:
        if line.startswith("SPEAKER"):
            parts = line.split(" ")
            speaker = parts[0] + " " + parts[1]  # Combining SPEAKER and number
            text = " ".join(parts[3:])  # The rest is the spoken text
            if speaker in diarisation_data:
                # Append to existing text if the speaker is already present
                diarisation_data[speaker] += " " + text
            else:
                # Otherwise, start a new entry
                diarisation_data[speaker] = text
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
            "diarisation": [diarisation_data],  # diarisation maps to a string
            "analysis": [analysis_json] # Second element of the array
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()
    except requests.RequestException as e:
        return {'error': str(e)}

def create_indicator_diarisation2(id, rtype, diarisation, analysis):
    url = "https://salescrmbe.onrender.com/api/create-diarisation"
    headers = {'Content-Type': 'application/json'}

    # Extracting the diarisation string
    diarisation_string = next(iter(diarisation.values())) if isinstance(diarisation, dict) else diarisation

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
            "diarisation": diarisation_string,  # diarisation maps to a string
            "analysis": [analysis_json] # Second element of the array
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()
    except requests.RequestException as e:
        return {'error': str(e)}

# Example usage
# upload_analysis = create_indicator_diarisation(str(id), rtype, diarisation, recording_analysis)
# print('upload_analysis', upload_analysis)

def create_indicator_diarisation1(id, rtype, diarisation, analysis):
    url = "https://salescrmbe.onrender.com/api/create-diarisation"
    headers = {'Content-Type': 'application/json'}
     
    # Finding the start and end of the JSON content
    json_start = analysis.find('{')
    json_end = analysis.rfind('}') + 1  # +1 to include the closing brace

    # Extracting the JSON part
    json_part = analysis[json_start:json_end]

    # Parsing the JSON string
    try:
        analysis_json = json.loads(json_part)
        print("Parsed JSON:", analysis_json)
    except json.JSONDecodeError as e:
        print("Error decoding JSON string:", e)

    # Construct the payload with diarisation and analysis inside the 'data' field
    payload = {
        "id": id,
        "type": rtype,
        "data": {
            "diarisation": diarisation,  # Adding diarisation inside 'data'
            "analysis": analysis_json         # Adding analysis inside 'data'
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()
    except requests.RequestException as e:
        return {'error': str(e)}


def create_indicator_diarisation_old(id, recording_analysis):
    url = "https://salescrmbe.onrender.com/api/create-diarisation"
    headers = {'Content-Type': 'application/json'}
     
    # Construct the payload
    payload = {
        "id": id,
        "type": "indicator",
        "data": recording_analysis
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response.json()
    except requests.RequestException as e:
        return {'error': str(e)}




















# Example usage
'''task_id = 'your_task_id'  # Replace with your actual task ID
result = get_diarization_result(task_id)
print(result)

print(response.text)'''




# Example usage
#url = "http://example.com/upload"  # Replace with your actual URL
#file_path = "path/to/recording.wav"  # Replace with the path to your .wav file
#id = "12345"  # Replace with your actual ID

#response = send_post_request(url, file_path, id)
#print(response.text)


"""
    Send a POST request to the specified URL with a file and an ID.

    Parameters:
    url (str): The URL to which the POST request is sent.
    file_path (str): The path to the .wav file to be sent.
    id (str): The ID to be sent along with the file.

    Returns:
    response: The response object from the server."""