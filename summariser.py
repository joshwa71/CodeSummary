import os
import shutil
import requests
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Convert files and interact with GPT-4.')
parser.add_argument('--api_key', type=str, required=True, help='Your OpenAI API key')
args = parser.parse_args()

# Use the API key from command-line arguments
OAI_api_key = args.api_key

# Path to the folder containing files to be converted
source_folder_path = './test_folder'

# Path to the temp folder where .txt files will be saved
temp_folder_path = './temp'

# Check if the temp folder exists, create it if not
if not os.path.exists(temp_folder_path):
    os.makedirs(temp_folder_path)

# Check if the source folder exists
if os.path.exists(source_folder_path):
    for filename in os.listdir(source_folder_path):
        file_path = os.path.join(source_folder_path, filename)
        if os.path.isfile(file_path):
            new_file_name = os.path.splitext(filename)[0] + '.txt'
            new_file_path = os.path.join(temp_folder_path, new_file_name)
            shutil.copy(file_path, new_file_path)
            print(f"Converted {filename} to {new_file_name} in {temp_folder_path}")

    # GPT-4 API interaction
    summaries = []
    for filename in os.listdir(temp_folder_path):
        file_path = os.path.join(temp_folder_path, filename)
        
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r') as f:
                file_text = f.read()
            
            prompt = f"This code file is part of a repository. Summarize this code so that summary can be used to write a README.me. Your summary should be thorough but concise - give a description of the file, its purpose and functionality, then follow this with  breakdown of the imports, classes and functions, anything that would be useful to write a README.me:\n{file_text}"
            gpt_response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={'Authorization': f'Bearer {OAI_api_key}'},
                json={
                    'model': 'gpt-4',
                    'messages': [{'role': 'user', 'content': prompt}]
                }
            )
            response_content = gpt_response.json()['choices'][0]['message']['content']
            summaries.append(filename[:-4] + ' : ' + response_content)
        
    prompt = f"Here is a list of code filenames and their summaries for a GitHub repository: {summaries}. Write a README.md using these summaries."
    gpt_response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {OAI_api_key}'},
        json={
            'model': 'gpt-4',
            'messages': [{'role': 'user', 'content': prompt}]
        }
    )
    response_content = gpt_response.json()['choices'][0]['message']['content']
    print(f"README.md content: {response_content}")

    # Delete the temp folder
    shutil.rmtree(temp_folder_path)
    print(f"Deleted the temp folder: {temp_folder_path}")

else:
    print(f"Folder {source_folder_path} does not exist.")
