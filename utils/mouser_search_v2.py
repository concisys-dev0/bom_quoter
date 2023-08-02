from utils.mouser_apiKeys import*
import os
import sys
import re
import requests
import json

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)

"""API operations related to search product information from version 2"""
ver2 = "v2"

def write_mouser_keyword_manufacturer_json(key_manufacturer_file):
    access_file = 'mouser_key_manufacturer_info.json'
    with open(access_file, 'w') as file:
        json.dump(key_manufacturer_file, file, indent=4)

def write_mouser_part_manufacturer_json(part_manufacturer_file):
    access_file = 'mouser_part_manufacturer_info.json'
    with open(access_file, 'w') as file:
        json.dump(part_manufacturer_file, file, indent=4)

def write_mouser_manufacturer_list_json(manufacturer_file):
    access_file = 'mouser_manufacturer_info.json'
    with open(access_file, 'w') as file:
        json.dump(manufacturer_file, file, indent=4)

# Search parts by keyword and specific manufacturer
def mouser_keyword_manufacturer(keyword, manufacturer):
    apiKey = get_current_apiKey() # to get apiKey
    request = {"SearchByKeywordMfrNameRequest": 
               {"manufacturerName": manufacturer,
                "keyword": keyword,
                "records": 50,
                "pageNumber": 0,
                "searchOptions": "string",
                "searchWithYourSignUpLanguage": "English"}
              }
    headers = {
        'accept' : 'application/json',
        'Content-Type' : 'application/json'
    }
    url = "https://api.mouser.com/api/" + ver2 + "/search/keywordandmanufacturer?apiKey=" + apiKey
    response = requests.post(url, json=request, headers=headers, verify=False) #, timeout=10
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
        
    key_manufacturer_file = response.json()
    key_manufacturer_info = write_mouser_keyword_manufacturer_json(key_manufacturer_file) # save response info
    # print(response.status_code)
    return key_manufacturer_file

# Search parts by part number and specific manufacturer
def mouser_part_manufacturer(part_id, manufacturer):
    apiKey = get_current_apiKey() # to get apiKey
    request = {
        "SearchByPartMfrNameRequest": 
        {"manufacturerName": manufacturer,
         "mouserPartNumber": part_id,
         "partSearchOptions": "string"}
    }
    headers = {
        'accept' : 'application/json',
        'Content-Type' : 'application/json'
    }
    url = "https://api.mouser.com/api/" + ver2 + "/search/partnumberandmanufacturer?apiKey=" + apiKey
    response = requests.post(url, json=request, headers=headers, verify=False) #, timeout=10
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
        
    part_manufacturer_file = response.json()
    part_manufacturer_info = write_mouser_part_manufacturer_json(part_manufacturer_file) # save response info
    # print(response.status_code)
    return part_manufacturer_file

# Get all Manufacturer List, return Manufacturer Name only.
def mouser_manufacturer_list():
    apiKey = get_current_apiKey() # to get apiKey
    headers = {
        'accept' : 'application/json'
    }
    url = "https://api.mouser.com/api/" + ver2 + "/search/manufacturerlist?apiKey=" + apiKey
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
    manufacturer_info = write_mouser_manufacturer_list_json(manufacturer_file) # save response info
    # print(response.status_code)
    return manufacturer_file

"""TEST CASE"""
# manufacturer = "Texas Instruments"
# keyword = "TPS54240DGQR"
# key_manufacturer_file = mouser_keyword_manufacturer(keyword, manufacturer)

# manufacturer = "Texas Instruments"
# part_id = "TPS54240DGQR"
# part_manufacturer_file = mouser_part_manufacturer(part_id, manufacturer)

# manufacturer_file = mouser_manufacturer_list()
