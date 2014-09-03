#!/usr/bin/python

# See: https://google-api-python-client.googlecode.com/hg/docs/epy/oauth2client.client.SignedJwtAssertionCredentials-class.html
# Example: http://www.jaco.it/blog/2013/05/31/google-api-oauth-2-dot-0-the-short-way
# import required classes
import httplib2
import os

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import SignedJwtAssertionCredentials 

# Declare constants and set configuration values

# Keyfile down-loaded from the console.
# Console is located here:
# 
PRIVATE_KEY_PATH = '../../private_data/ga_server_application/langstroth-user-statistics-1b19aa01b24f.p12'
TOKEN_STORAGE_PATH = '../../private_data/ga_server_application/analytics.dat'
SERVICE_ACCOUNT_EMAIL = '867155185349-vk8pvlfdnci5ok1oiot0fn8li5qsaeb7@developer.gserviceaccount.com'
# CLIENT_ID not used.
CLIENT_ID = '867155185349-vk8pvlfdnci5ok1oiot0fn8li5qsaeb7.apps.googleusercontent.com'

def prepare_credentials(): 
         
    http = httplib2.Http()
    
    storage = Storage(os.path.join(os.path.dirname(__file__), TOKEN_STORAGE_PATH))
    credentials = storage.get()    
    if credentials is None or credentials.invalid:
        with open(os.path.join(os.path.dirname(__file__), PRIVATE_KEY_PATH), "rb") as key_file:
            crypto_key = key_file.read()
        credentials = SignedJwtAssertionCredentials(SERVICE_ACCOUNT_EMAIL, crypto_key, scope='https://www.googleapis.com/auth/analytics.readonly')
        storage.put(credentials)
    else:
        credentials.refresh(http)

    http = credentials.authorize(http)  
    return http

def initialize_service():       
    http = prepare_credentials() 
    return build('analytics', 'v3', http=http)



