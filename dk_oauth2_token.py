from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import requests
import json
import webbrowser
import schedule
import time
import sys
import os

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)

authorize_url = "https://api.digikey.com/v1/oauth2/authorize"
token_url = "https://api.digikey.com/v1/oauth2/token"

callback_uri = "https://localhost/" #redirect uri

test_api_url = "https://api.digikey.com/" #host

client_id = 'jhZJWxD67jf2ONa8MAzE6eQAC8UtR1bM'
# tester1: 'B7oWwd6qhoswuTNKR5XNjVOJgavWhqG3'
# ldo:'jhZJWxD67jf2ONa8MAzE6eQAC8UtR1bM' 
# excess: 'v96weKvwrkhbxsufdcrABCd7tMT4wfuj'
client_secret = 'P832b8biNWfcNwCz'
# tester1: '4vM0yeVKQINod3gk'
# ldo:'P832b8biNWfcNwCz' 
# excess: 'DBKjJZIlxgaaGBaF'

def authorize_digikey_api(auth_url, client_id, redirect_uri):
    # set up the OAuth2Session object
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
    # get the authorization URL
    authorization_url, state = oauth.authorization_url(auth_url)
    webbrowser.open(authorization_url)
    return

def write_digikey_token(token):
    access_file = 'digikey_token.json'
    # with open(access_file, 'r') as read_file:
    #     old_token = json.load(read_file)
    with open(access_file, 'w') as file:
        json.dump(token, file, indent=4)
        
def token_digikey_api(auth_url, token_url, client_id, client_secret, redirect_uri):
    authorization_redirect_url = authorize_digikey_api(authorize_url, client_id, callback_uri)
    redirect_url = input("Enter the callback URL generates in the browser: ")
    authorization_code = redirect_url.split('?code=')[1].split('&')[0]
    print(authorization_code) #Debug

    data = {'code': authorization_code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': callback_uri,
            'grant_type': 'authorization_code'}
    access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
    #Debug print(access_token_response.headers)
    print(access_token_response.text)
    #Return failed message and failed status code if response is not 200
    if access_token_response.status_code != 200:
        return "Failed to obtain access token due to error:", access_token_response.status_code
    else:
        #Return the access token and writes the response into a json file is 200
        tokens = access_token_response.json()
        access_token = write_digikey_token(tokens)
        #Debug print(tokens['access_token']) 
        return tokens['access_token']
    
def refresh_token_digikey_api():
    with open('digikey_token.json', 'r') as file:
        old_token = json.load(file)
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 
               'Accept': 'application/json'}
    data = {'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': old_token['refresh_token'],
            'grant_type': 'refresh_token'}
    refresh_response = requests.post(token_url, data=data, headers=headers)
    if refresh_response.status_code != 200:
        return "Failed to obtain refresh token due to error: ", refresh_response.status_code
    else:
        refresh = refresh_response.json()
        refresh_token = write_digikey_token(refresh)
        return print(refresh['access_token'])
    
def refresh_token_timer():
    schedule.every(30).minutes.do(refresh_token_digikey_api)
    while True:
        schedule.run_pending()
        time.sleep(1)
    
"""TEST CASE"""
# token = token_digikey_api(authorize_url, token_url, client_id, client_secret, callback_uri)
# refresh_token_digikey_api()
# re_token = refresh_token_timer()
