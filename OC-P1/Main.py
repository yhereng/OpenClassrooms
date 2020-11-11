# -*- coding: utf-8 -*-
# This simple app uses the '/detect' resource to identify the language of
# the provided text or texts.

import os, requests, uuid, json



# Check if the environment variables exist

key_var_name = 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY'
if not key_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
subscription_key = os.environ[key_var_name]

endpoint_var_name = 'TRANSLATOR_TEXT_ENDPOINT'
if not endpoint_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
endpoint = os.environ[endpoint_var_name]

# Construction of Request URL
path = '/detect?api-version=3.0'
constructed_url = endpoint + path

# Required and optional header
headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,  #The value is the Azure secret key for your multi-service resource
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

print(detect_language("la vita e bella"))



