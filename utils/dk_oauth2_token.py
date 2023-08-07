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

from utils.dk_oauth2_login import *
from utils.constants import DK_USER_STORAGE, DK_TOKEN_STORAGE

# get access token and connect to API
dk_authorize_url = "https://api.digikey.com/v1/oauth2/authorize"
dk_token_url = "https://api.digikey.com/v1/oauth2/token"

def get_digikey_user():
    """ Returns the first digikey user in the json file, default to be active user of access token """
    try:
        with open(DK_USER_STORAGE, 'r') as file:
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

def retry_user(user_data, authorize_url=None, token_url=None):
    """ Retry authentication with other user's stored, append the old active user to the end """
    with open(DK_USER_STORAGE, 'r') as file:
        u_list = json.load(file)
        u_list.pop(u_list.index(user_data)) # remove unworking user from the list temporarily
    if len(u_list) == 0:
        write_digikey_user()
    # try the next user in the list
    for i in range(len(u_list)):
        n_user = u_list[i] # the next user in the list                                          
        if authorize_url is None:
            authorize_url = dk_authorize_url                                        
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
                u_list.append(user_data) # .index
                with open(DK_USER_STORAGE, 'w') as file:
                    json.dump(u_list, file) # add unworking user back to end of the list
                return access_token_response
        except Exception as e:
            print(f"Failed to obtain access token for Digi-Key {n_user['name']} due to error: \n{str(e)}")
            if i > len(u_list):
                # Return error message when list is finished and no valid access
                return print(f"Failed to obtain access token for Digi-Key users due to error: " + str(e))
            continue # continue to the next user if i <= len(u_list)
 
def authorize_digikey_api(auth_url, client_id, redirect_uri, username, password):
    """ Return the access token url to get the token response that will parse to json """
    # set up the OAuth2Session object
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
    # get the authorization URL
    authorization_url, state = oauth.authorization_url(auth_url)
    access_token_url = digikey_login(authorization_url, username, password) # login automation
    # webbrowser.open(authorization_url)
    return access_token_url

def write_digikey_token(token):
    """ Save all the token response info to digikey_token.json """
    with open(DK_TOKEN_STORAGE, 'w') as file:
        json.dump(token, file, indent=4)

def token_digikey_api(auth_url=None, token_url=None):
    """ Get access token from user info and connect with API """
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
    # Authorize Automation by user - deprecation
    # authorization_redirect_url = authorize_digikey_api(authorize_url, client_id, callback_uri)
    # redirect_url = input("Enter the callback URL generates in the browser: ")
    access_token_url = authorize_digikey_api(auth_url, client_id, redirect_uri, username, password)
    print(access_token_url) # debug
    try:
        authorization_code = access_token_url.split('?code=')[1].split('&')[0]
        # print(authorization_code) #Debug
    except IndexError:
        raise IndexError("Authentication failed because it was unable to get a valid access code")
    print("Authorization code: " + authorization_code)
    data = {'code': authorization_code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'}
    access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
    print(access_token_response.headers) # Debug 
    print(access_token_response.text)
    #Return failed message and failed status code if response is not 200
    if access_token_response.status_code != 200:
        access_token_response = retry_user(dkuser)
    # Otherwise, return the access token and writes the response into a json file is 200
    tokens = access_token_response.json()
    access_token = write_digikey_token(tokens)
    #Debug print(tokens['access_token']) 
    return tokens['access_token']

def refresh_token_digikey_api(token_url=None):
    """ Get new access token from refresh token when current access token expired """
    with open(DK_TOKEN_STORAGE, 'r') as file:
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


def refresh_token_timer(): # Infinite function, need to set up schedule for it to stop and run without error or set the host to be never sleep
    """ Run refresh_token_digikey_api every 30 min interval to automate new access token """
    schedule.every(30).minutes.do(refresh_token_digikey_api)
    while True:
        schedule.run_pending()
        time.sleep(1)

# L Version:
# def get_change_user(err_m):
#     error_messages = ['Daily Ratelimit exceeded', 'The Bearer token is invalid']
#     if err_m in error_messages:
#         ex_user = get_digikey_user()
#         access_token_response = retry_user(ex_user)
#         tokens = access_token_response.json()
#         access_token = write_digikey_token(tokens)
#         return tokens['access_token']
#     else:
#         return None

# M Version:
def get_change_user():
    """ Return access token from new active user """
    ex_user = get_digikey_user()
    access_token_response = retry_user(ex_user)
    tokens = access_token_response.json()
    access_token = write_digikey_token(tokens)
    return tokens['access_token']
    
"""TEST CASE"""
# if __name__ == "__main__":
#     start_time = time.time()
#     token_digikey_api() #can't work with headless
#     refresh_token_digikey_api()
#     # re_token = refresh_token_timer()
#     get_change_user(err_m = "Daily Ratelimit exceeded")
#     print("--- %s seconds ---" % (time.time() - start_time))