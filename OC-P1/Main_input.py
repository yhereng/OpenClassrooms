# -*- coding: utf-8 -*-
# This simple app uses the '/detect' resource to identify the language of
# the provided text or texts.

import os, requests, uuid, json

#Package used to get environment variables
from dotenv import load_dotenv
load_dotenv() # load Variable from .env file to local environment

# Check if the environment variables exist
key_var_name = "TRANSLATOR_TEXT_SUBSCRIPTION_KEY"
if not key_var_name in os.environ:
  raise Exception('Could not find your API key in the .env file')
secret_key=os.getenv(key_var_name)

endpoint_var_name ='TRANSLATOR_TEXT_ENDPOINT'
if not endpoint_var_name in os.environ:
    raise Exception('Could not find the endpoint API address in the .env file')
endpoint = os.getenv(endpoint_var_name)

# Construction of Request URL
path = '/detect?api-version=3.0' #in this case we use the detect function of the API
constructed_url = endpoint + path

# Required and optional header
headers = {
    'Ocp-Apim-Subscription-Key': secret_key,  #The value is the Azure secret key for your multi-service resource
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())            #Optional to uniquely identify the request
}

# Function that send the request and return a tuple with the identified language as str and score as float

def detect_language(texte):
    body = [{'text': texte}]
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    return(
        response[0]['language'],
        response[0]['score']
    )

#calling the function with your text and printing answer

text = input("enter your text: ")

print("----------------")
print("detected language and confidence level")
print(detect_language(text))



