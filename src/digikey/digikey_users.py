from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)
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
from random import randint

from src.utils.digikey_driver import driver_setup

#global variables
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/111.0.0.0 Safari/537.36"

# Login Automation
def user_login(auth_url, username, password):
    browser = driver_setup()
    browser.get(auth_url)
    time.sleep(randint(2,10))
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": USER_AGENT})
    wait = WebDriverWait(browser, 5)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'logo-frame')))
    print("Logging in. Please wait..")
    user_field = browser.find_element(By.CSS_SELECTOR, 'input#username')
    pass_field = browser.find_element(By.CSS_SELECTOR, 'input#password')
    submit_button = browser.find_element(By.CSS_SELECTOR, 'a#signOnButton')
    time.sleep(1)
    user_field.send_keys(username)
    pass_field.send_keys(password)
    time.sleep(1)
    submit_button.click()
    time.sleep(2)
    auth_code_url = browser.current_url
    browser.quit()
    return auth_code_url

# Save new digikey user login    
def write_new_user():
    print("WARNING: Please keep Digi-Key login information private. Don't share credentials or save it on a shared device.")
    name = str(input("Enter your first name only: "))
    username = str(input("Enter Digi-Key username/email: "))
    password = str(input("Enter password: "))
    client_id = str(input("Client ID: "))
    client_secret = str(input("Client Secret: "))
    callback_url = str(input("Enter Callback URL: "))
    user_auth = {
        'name': name,
        'redirect_uri': callback_url,
        'username': username,
        'password': password,
        'client_id': client_id,
        'client_secret': client_secret
    }
    user_file = r'..//src//auth//digikey_user.json'
    # print(user_auth)
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
    print("New Digikey user added. You are now using the new user credentials.")
    return user_auth

