import streamlit as st
import requests
from dotenv import load_dotenv
import os
import json
load_dotenv()

key_var_name = "MODEL_ENDPOINT"
if not key_var_name in os.environ:
  raise Exception('Could not find your endpoint in .env file')
uri=os.getenv(key_var_name)

def get_response(texts,uri):
    #make the texts as json
    request=build_json(texts)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(uri, request,headers=headers)
    return response

def build_json(texts):
    '''texts mut be of format [string]'''
    i=1
    dict_text={}
    for text in texts:
        dict_text[i]=text
        i+=1
    return json.dumps({"text":dict_text})

def show_response(texts,uri):
    response=get_response(texts,uri)
    for text,pred in zip(texts,get_response(texts,uri).json()):
        st.text(f'{text}---> sentiment: {pred}')



user_input = st.text_input("Please type tweet to be analysed")

show_response([user_input],uri)