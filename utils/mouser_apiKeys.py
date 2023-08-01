import os
import sys
import re
import requests
import json
from json.decoder import JSONDecodeError
import time

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)

from utils.constants import MS_USER_STORAGE

"""Handle user information and change user’s API key when need"""
# Add mouser user info to json
def write_mouser_user():
    print("WARNING: Please keep Mouser information private. Don't share credentials or save it on a shared device.")
    name = str(input("Enter your first name only: "))
    username = str(input("Enter Mouser username: "))
    password = str(input("Enter password: "))
    apiKey = str(input("Enter API key: "))
    user_auth = {
        'name': name,
        'username': username,
        'password': password,
        'apiKey': apiKey,
        'status': "Idle"
    }
    # user_file = 'mouser_user.json'
    user_file = MS_USER_STORAGE
    print(user_auth)
    if not os.path.exists(user_file):
        # if file doesn't exist, we'll make a new one
        with open(user_file, 'w') as userjson:
            users_data = [user_auth] # converting the dictionary into list of dictionary
            json.dump(users_data, userjson, indent=4)
    else:
        with open(user_file) as userjson:
            try:
                users_data = json.load(userjson) # load user list
                users_data.append(user_auth) # add the new user to the list
                # print(users_data) # debug
                with open(user_file, 'w') as newjson:
                    # Overwrite the file with the list w/ new user data
                    json.dump(users_data, newjson, indent=4, separators=(',',': '))
            except JSONDecodeError:
                # if the file exists but is empty, we'll add the new user data in it
                print("json error")
                with open(user_file, 'w') as newjson:
                    users_data = [user_auth]
                    json.dump(users_data, newjson, indent=4, separators=(',',': '))
    print("New Mouser user added. You are now using the new user credentials.")
    return user_auth

# Function return the status of apiKey by index
def get_apiKey_status(key_index):
    try:
        with open(MS_USER_STORAGE, 'r') as file:
            user_list = json.load(file) # list of mouser users
            if len(user_list) > 0:
                if key_index < len(user_list):
                    user = user_list[key_index] # take the first
                else:
                    return "Index Out of Range"
            else:
                user = write_mouser_user()
    except JSONDecodeError:
        user = write_mouser_user()
    except FileNotFoundError:
        user = write_mouser_user()
    except Exception as e:
        raise e
    return user['status']

# Function return the  index of current user have status active
def get_keyIndex_Active():
    try:
        with open(MS_USER_STORAGE, 'r') as file:
            user_list = json.load(file) # list of mouser users
            if len(user_list) > 0:
                l = len(user_list)
                for i in range(l):
                    status = get_apiKey_status(i)
                    if str(status) == "Active":
                        key_index = i
                        return key_index
                    elif i == len(user_list)-1 and str(status) == "Idle": 
                        # only if all index status is "Idle"
                        # change status of first index as default
                        key_index = 0
                        user_list[0]['status'] = "Active"
                        with open(MS_USER_STORAGE, 'w') as file:
                            json.dump(user_list, file)
                        return key_index
            else:
                user = write_mouser_user()
    except JSONDecodeError:
        user = write_mouser_user()
    except FileNotFoundError:
        user = write_mouser_user()
    except Exception as e:
        raise e

# Function return the current apiKey
def get_current_apiKey():
    try:
        with open(MS_USER_STORAGE, 'r') as file:
            user_list = json.load(file) # list of mouser users
        keyIndex = get_keyIndex_Active()
        apiKey = user_list[keyIndex]['apiKey']
        return apiKey
    except JSONDecodeError:
        user = write_mouser_user()
    except FileNotFoundError:
        user = write_mouser_user()
    except Exception as e:
        raise e

# Function change apiKey and status
def change_apiKey_Active(err_m):
    if err_m == "Maximum calls per day exceeded.":
        expire_keyIndex = get_keyIndex_Active()
        with open(MS_USER_STORAGE, 'r') as file:
            user_list = json.load(file) # list of mouser users
        if len(user_list) == 1: # when it's only user
            print("please add more user")
            apiKey = get_current_apiKey()
            return apiKey
            # new_user = write_mouser_user()
        if len(user_list)-1 > expire_keyIndex:
            next_index = expire_keyIndex + 1
        elif len(user_list)-1 == expire_keyIndex: # expire_keyIndex is last index element
            next_index = 0
        user_list[expire_keyIndex]['status'] = "Idle"
        user_list[next_index]['status'] = "Active"
        with open(MS_USER_STORAGE, 'w') as file:
            json.dump(user_list, file)
        # current_index = next_index
        apiKey = get_current_apiKey()
        return apiKey
    else:
        return None

"""TEST CASE"""
# write_mouser_user()
# print(get_apiKey_status(key_index=1))
# print(get_keyIndex_Active())
# print(get_current_apiKey())
# print(change_apiKey_Active(err_m = "Maximum calls per day exceeded."))