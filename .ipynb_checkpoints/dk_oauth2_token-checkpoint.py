from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import requests
import json
from json.decoder import JSONDecodeError
import webbrowser
import schedule
import time
import sys
import os

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)
from dk_oauth2_login import digikey_login, write_digikey_user

dk_authorize_url = "https://api.digikey.com/v1/oauth2/authorize"
dk_token_url = "https://api.digikey.com/v1/oauth2/token"

# callback_uri = "https://localhost/" #redirect uri
# test_api_url = "https://api.digikey.com/" #host
# client_id = 'jhZJWxD67jf2ONa8MAzE6eQAC8UtR1bM'
# tester1: 'B7oWwd6qhoswuTNKR5XNjVOJgavWhqG3'
# ldo:'jhZJWxD67jf2ONa8MAzE6eQAC8UtR1bM' 
# excess: 'v96weKvwrkhbxsufdcrABCd7tMT4wfuj'
# client_secret = 'P832b8biNWfcNwCz'
# tester1: '4vM0yeVKQINod3gk'
# ldo:'P832b8biNWfcNwCz' 
# excess: 'DBKjJZIlxgaaGBaF'

# Returns the first digikey user in the json file
def get_digikey_user():
    try:
        with open('digikey_user.json', 'r') as file:
            user_list = json.load(file) # list of digikey users
            if len(user_list) > 0:
                user = user_list[0] # take the first
            else:
                user = write_digikey_user()
    except JSONDecodeError:
        user = write_digikey_user()
    except FileNotFoundError:
        user = write_digikey_user()
    except Exception as e:
        raise e
    return user

# retry authentication with other user's stored
def retry_user(user_data, authorize_url=None, token_url=None):
    with open('digikey_user.json', 'r') as file:
        u_list = json.load(file)
        u_list.pop(u_list.index(user_data)) # remove unworking user from the list temporarily
    if len(u_list) == 0:
        write_digikey_user()
    # try the next user in the list
    for i in range(len(u_list)):
        n_user = u_list[i] # the next user in the list
        # authorize_url = n_user['auth_url']
        if authorize_url is None:
            authorize_url = dk_authorize_url
        # token_url = n_user['token_url']
        if token_url is None:
            token_url = dk_token_url
        client_id = n_user['client_id']
        client_secret = n_user['client_secret']
        redirect_uri = n_user['redirect_uri']
        username = n_user['username']
        password = n_user['password']
        try:
            access_token_url = authorize_digikey_api(authorize_url, client_id, redirect_uri, username, password)
            authorization_code = access_token_url.split('?code=')[1].split('&')[0]
            data = {'code': authorization_code,
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'redirect_uri': redirect_uri,
                    'grant_type': 'authorization_code'}
            access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
            # print(access_token_response.text) # debug
            if access_token_response.status_code == 200:
                # first valid response is returned
                return access_token_response
        except Exception as e:
            print(f"Failed to obtain access token for Digi-Key {n_user['name']} due to error: \n{str(e)}")
            if i > len(u_list):
                # Return error message when list is finished and no valid access
                return print(f"Failed to obtain access token for Digi-Key users due to error: " + str(e))
            continue # continue to the next user if i < len(u_list)
        
def authorize_digikey_api(auth_url, client_id, redirect_uri, username, password):
    # set up the OAuth2Session object
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
    # get the authorization URL
    authorization_url, state = oauth.authorization_url(auth_url)
    access_token_url = digikey_login(authorization_url, username, password) # login automation
    # webbrowser.open(authorization_url)
    return access_token_url

def write_digikey_token(token):
    access_file = 'digikey_token.json'
    # with open(access_file, 'r') as read_file:
    #     old_token = json.load(read_file)
    with open(access_file, 'w') as file:
        json.dump(token, file, indent=4)
        
def token_digikey_api(auth_url=None, token_url=None):
    dkuser = get_digikey_user()
    if auth_url is None:
        auth_url = dk_authorize_url
    if token_url is None:
        token_url = dk_token_url
    client_id = dkuser['client_id']
    client_secret = dkuser['client_secret']
    redirect_uri = dkuser['redirect_uri']
    username = dkuser['username']
    password = dkuser['password']
    # Authorize Automation
    # authorization_redirect_url = authorize_digikey_api(authorize_url, client_id, callback_uri)
    # redirect_url = input("Enter the callback URL generates in the browser: ")
    access_token_url = authorize_digikey_api(auth_url, client_id, redirect_uri, username, password)
    # print(access_token_url) # debug
    try:
        authorization_code = access_token_url.split('?code=')[1].split('&')[0]
        print(authorization_code) #Debug
    except IndexError:
        raise IndexError("Authentication failed because it was unable to get a valid access code")
    print("Authorization code: " + authorization_code)
    data = {'code': authorization_code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'}
    access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
    #Debug print(access_token_response.headers)
    print(access_token_response.text)
    #Return failed message and failed status code if response is not 200
    if access_token_response.status_code != 200:
        # return "Failed to obtain access token due to error:", access_token_response.status_code
        access_token_response = retry_user(dkuser)
    #Return the access token and writes the response into a json file is 200
    tokens = access_token_response.json()
    access_token = write_digikey_token(tokens)
    #Debug print(tokens['access_token']) 
    return tokens['access_token']

def refresh_token_digikey_api(token_url=None):
    with open('digikey_token.json', 'r') as file:
        old_token = json.load(file)
    user = get_digikey_user()
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 
               'Accept': 'application/json'}
    data = {'client_id': user['client_id'],
            'client_secret': user['client_secret'],
            'refresh_token': old_token['refresh_token'],
            'grant_type': 'refresh_token'}
    if token_url is None:
        token_url = dk_token_url
    refresh_response = requests.post(token_url, data=data, headers=headers)
    if refresh_response.status_code != 200:
        # return "Failed to obtain refresh token due to error: ", refresh_response.status_code
        try:
            refresh_response = retry_user(user)
        except:
            return "Failed to obtain refresh token due to error: ", refresh_response.status_code
    else:
        refresh = refresh_response.json()
        refresh_token = write_digikey_token(refresh)
        return print("Refresh access token:", refresh['access_token'])
    
def refresh_token_timer():
    schedule.every(30).minutes.do(refresh_token_digikey_api)
    while True:
        schedule.run_pending()
        time.sleep(1)
    
"""TEST CASE"""
# if __name__ == "__main__":
#     token = token_digikey_api()
#     # refresh_token_digikey_api()
#     re_token = refresh_token_timer()
