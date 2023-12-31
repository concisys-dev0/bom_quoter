import requests
import json
import sys
import os
import re

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)

"""API operations related to search product information"""
apiKey = "7328553502494f9c83c51c3188acf585" # Subscription key

# def write_tti_keyword_json(keyword_file):
#     access_file = 'tti_keyword_info.json'
#     with open(access_file, 'w') as file:
#         json.dump(keyword_file, file, indent=4)
        
# def write_tti_manufacturer_list_json(manufacturer_file):
#     access_file = 'tti_manufacturer_info.json'
#     with open(access_file, 'w') as file:
#         json.dump(manufacturer_file, file, indent=4)

# Search for parts by keyword including part number, manufacturer, or category to see a list of parts matching the term
def tti_SearchByKeyword(keyword):
    params = {'searchTerms' : keyword, 
              'customerAccountNumber' : 'CAC057', 
              'requestEntity' : 'NA'
             }
    headers = {'accept' : 'application/json', 
               'Content-Type' : 'application/json', 
               'apiKey' : apiKey
              }
    url = "https://api.tti.com/service/api/v1/search/keyword?searchTerms="
    response = requests.get(url, params=params, headers=headers, verify=False) #, timeout=10
    if response.status_code != 200: # HTTP connection error
        r = json.loads(response.text)
        # print error message
        if 'Details' in r:
            print(response.status_code)
            s = r['Details']
        elif 'moreInformation' in r:
            print(response.status_code)
            s = r['moreInformation']
        elif 'message' in r:
            print(response.status_code)
            s = r['message']
        else:
            print(response.status_code)
            s = r['ErrorMessage']
        # raise Exception(s)
        
    keyword_file = response.json()
    # keyword_info = write_tti_keyword_json(keyword_file) # save response info
    return keyword_file

# Retrieve a list of manufacturer names and manufacturer codes
def tti_manufacturer_list():
    headers = {'accept' : 'application/json', 
               'apiKey' : apiKey
              }
    url = "https://api.tti.com/service/api/v1/search/manufacturers"
    response = requests.get(url, headers=headers, verify=False) #, timeout=10
    if response.status_code != 200: # HTTP connection error
        r = json.loads(response.text)
        # print error message
        if 'Details' in r:
            print(response.status_code)
            s = r['Details']
        elif 'moreInformation' in r:
            print(response.status_code)
            s = r['moreInformation']
        elif 'message' in r:
            print(response.status_code)
            s = r['message']
        else:
            print(response.status_code)
            s = r['ErrorMessage']
        # raise Exception(s)
        
    manufacturer_file = response.json()
    # manufacturer_info = write_tti_manufacturer_list_json(manufacturer_file) # save response info
    return manufacturer_file

"""TEST CASE"""
# keyword = "TR3D476K025D0100"
# keyword_file = tti_SearchByKeyword(keyword)

# manufacturer_file = tti_manufacturer_list()