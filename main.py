import requests
from dotenv import load_dotenv
import os
from email_report import report
import sys
# Load environment variables from .env file
load_dotenv()


# Define the base URL, defaulting to 'http://127.0.0.1:5000' if not present in .env
base_url = os.getenv('BASE_URL', 'http://127.0.0.1:5000')

# Print the base URL for debugging purposes
print(f"Base URL: {base_url}")

cwd = os.getcwd()
print(cwd)

# TESTING LLM ENDPOINTS
print('Testing LLM Endpoints.....')
# Initialize the session
session = requests.Session()

#upload endpoint test
try:
    # 1. Upload the file
    upload_url = f'{base_url}/upload'
    file_path = f'{cwd}/test files/test.csv'

    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = session.post(upload_url, files=files)
        response_json = response.json()
        print("Upload response:", response_json)

    # 2. Validate the response
    expected_message = 'File uploaded successfully'
    expected_filename = os.path.basename(file_path)  # Extract filename from the file path

    if response_json.get('message') == expected_message and response_json.get('filename') == expected_filename:
        success = True
    else:
        success = False

    # Report the outcome
    report('/upload', success, response_json)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    success = False
    report('/upload', success, str(e))



#retrieve files endpoint test
try:
    # 2. Retrieve the list of uploaded files
    retrieve_files_url = f'{base_url}/retrieve-files'
    response = session.get(retrieve_files_url)
    print("Retrieve files response:", response.json())
    print()
    response_json = response.json()
    # Check if the response contains the specific failure message
    
    if 'files' in response_json and isinstance(response_json['files'], list):
        files = response_json['files']
        if len(files) > 0 and 'filename' in files[0]:
            success = True
        else:
            success = False
    else:
        success = False

    report('/retrieve-files', success, response.json())

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    success = False
    report('/retrieve-files', success, str(e))

#TODO: find a way to test the GPT response endpoint
#gpt-response endpoint test
try:
    #Get GPT-3 response
    gpt_response_url = f'{base_url}/gpt-response'
    data = {'user_message': 'Explain the content of the uploaded file'}
    response = session.post(gpt_response_url, json=data)
    print("GPT response:", response.json())
    print()
    #response_json = response.json()
    # Check if the response contains the specific failure message
    #if response_json.get('message') == 'Authorization token not provided':
        #success = False
    #else:
        #success = True

    report('/gpt-response', success, response.json())

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    success = False
    report('/gpt-response', success, str(e))




#TESTING Central Auth and PACK ENDPOINTS
print('\nTesting Pack Endpoints.....\n')
try:
    # Get GPT-3 pack response (assuming you have implemented the relevant logic in the endpoint)
    gpt_pack_response_url = f'{base_url}/gpt-pack-response'
    pack_data = {
        'user_message': 'Explain the pack content',
        'pack_id': 'example_pack_id',  # You will need to replace this with a valid pack ID
        'history': 'previous conversation history'
    }
    response = session.post(gpt_pack_response_url, json=pack_data)
    response_json = response.json()
    print("GPT pack response:", response_json)

    # Check if the response contains the specific failure message
    if response_json.get('message') == 'Authorization token not provided':
        success = False
    else:
        success = True

    # Call report function
    report('/gpt-pack-response', success, response_json)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    success = False
    report('/gpt-pack-response', success, str(e))


try:
    #Delete the session and all associated files
    delete_session_url = f'{base_url}/delete-session'
    response = session.delete(delete_session_url)
    response_json = response.json()
    print("Delete session response:", response_json)

    # Check if the response contains the specific failure message
    if response_json.get('message') != 'Session and all associated files deleted successfully':
        success = False
    else:
        success = True

    # Call report function
    report('/delete-session', success, response.json())

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    success = False
    report('/delete-session', success, str(e))