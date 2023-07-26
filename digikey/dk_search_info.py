from dk_oauth2_token import get_digikey_user
import requests
import json
import sys
import os

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)


def write_digikey_keyword_json(keyword_file): 
    """ saves keyword_info json"""
    access_file = 'digikey_keyword_info.json'
    with open(access_file, 'w') as fil:
        json.dump(keyword_file, fil, indent=4)
        
def get_digikey_part_info(part_id): # searches for part; param: part_id -> manufacturer part number
    """ Searches for part
    param: part_id -> mfg part number
    """
    with open('digikey_token.json', 'r') as file:
        token = json.load(file)
    if token['access_token'] is None:
        raise Exception("No Token Loaded")
    user = get_digikey_user()
    headers = {
        'accept' : 'application/json',
        'authorization' : 'Bearer ' + token['access_token'],
        'X-DIGIKEY-Client-Id' : user['client_id'],
        'X-DIGIKEY-Locale-Site' : 'US',
        'X-DIGIKEY-Locale-Language' : 'en',
        'X-DIGIKEY-Locale-Currency' : 'USD',
        'X-DIGIKEY-Locale-ShipToCountry' : 'US'
    }
    url = 'https://api.digikey.com/Search/v3/Products/' + part_id
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        r = json.loads(response.text)
        if 'Details' in r:
            s = r['Details']
            print(s)
        elif 'moreInformation' in r:
            s = r['moreInformation']
            print(s)
        elif 'message' in r:
            s = r['message']
            print(s)
        else:
            s = r['ErrorMessage']
            print(s)

    info_file = response.json()
    return info_file

def get_digikey_part_sub_info(part_id):
    with open('digikey_token.json', 'r') as file:
        token = json.load(file)
    if token['access_token'] is None:
        raise Exception("No Token Loaded")
    user = get_digikey_user()
    headers = {
        'accept' : 'application/json',
        'partNumber' : part_id,
        'authorization' : 'Bearer ' + token['access_token'],
        'X-DIGIKEY-Client-Id' : user['client_id'],
        'X-DIGIKEY-Locale-Site' : 'US',
        'X-DIGIKEY-Locale-Language' : 'en',
        'X-DIGIKEY-Locale-Currency' : 'USD',
        'X-DIGIKEY-Locale-ShipToCountry' : 'US'
    }
    url = 'https://api.digikey.com/Search/v3/Products/' + part_id + '/WithSuggestedProducts'
    response = requests.get(url, headers=headers) #, verify=False
    if response.status_code != 200:
        r = json.loads(response.text)
        if 'Details' in r:
            s = r['Details']
            print(s)
        elif 'moreInformation' in r:
            s = r['moreInformation']
            print(s)
        elif 'message' in r:
            s = r['message']
            print(s)
        else:
            s = r['ErrorMessage']
            print(s)
        
    sub_file = response.json()
    return sub_file

def get_digikey_reel_pricing(digikey_part, Qty):
    with open('digikey_token.json', 'r') as file:
        token = json.load(file)
    if token['access_token'] is None:
        raise Exception("No Token Loaded")
    user = get_digikey_user()
    params = {
        'digiKeyPartNumber' : digikey_part,
        'requestedQuantity' : Qty,
        'includes' : 'ExtendedPrice,ReelingFee,UnitPrice,SearchLocaleUsed'}
    headers = {
        'accept' : 'application/json',
        'Authorization' : 'Bearer ' + token['access_token'],
        'X-DIGIKEY-Client-Id' : user['client_id'],
        'X-DIGIKEY-Locale-Site' : 'US',
        'X-DIGIKEY-Locale-Language' : 'en',
        'X-DIGIKEY-Locale-Currency' : 'USD',
        'X-DIGIKEY-Locale-ShipToCountry' : 'US'
    }
    url = 'https://api.digikey.com/Search/v3/Products/' + digikey_part + '/DigiReelPricing'
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        r = json.loads(response.text)
        if 'Details' in r:
            s = r['Details']
            print(s)
        elif 'moreInformation' in r:
            s = r['moreInformation']
            print(s)
        elif 'message' in r:
            s = r['message']
            print(s)
        else:
            s = r['ErrorMessage']
            print(s)
        # raise Exception(s)
        
    return response.json()

def get_digikey_categories_search():
    with open('digikey_token.json', 'r') as file:
        token = json.load(file)
    if token is None:
        raise Exception("No Token Loaded")
    user = get_digikey_user()
    headers = {
        'accept' : 'application/json',
        'authorization' : 'Bearer ' + token['access_token'],
        'X-DIGIKEY-Client-Id' : user['client_id'],
        'X-DIGIKEY-Locale-Site' : 'US',
        'X-DIGIKEY-Locale-Language' : 'en',
        'X-DIGIKEY-Locale-Currency' : 'USD',
        'X-DIGIKEY-Locale-ShipToCountry' : 'US'
    }
    url = 'https://api.digikey.com/Search/v3/Categories'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        r = json.loads(response.text)
        if 'Details' in r:
            s = r['Details']
            print(s)
        elif 'moreInformation' in r:
            s = r['moreInformation']
            print(s)
        elif 'message' in r:
            s = r['message']
            print(s)
        else:
            s = r['ErrorMessage']
            print(s)
        
    categories_file = response.json()
    return categories_file
        
def get_digikey_manufacturers_search():
    with open('digikey_token.json', 'r') as file:
        token = json.load(file)
    if token is None:
        raise Exception("No Token Loaded")
    user = get_digikey_user()
    headers = {
        'accept' : 'application/json',
        'authorization' : 'Bearer ' + token['access_token'],
        'X-DIGIKEY-Client-Id' : user['client_id'],
        'X-DIGIKEY-Locale-Site' : 'US',
        'X-DIGIKEY-Locale-Language' : 'en',
        'X-DIGIKEY-Locale-Currency' : 'USD',
        'X-DIGIKEY-Locale-ShipToCountry' : 'US'
    }
    url = 'https://api.digikey.com/Search/v3/Manufacturers'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        r = json.loads(response.text)
        if 'Details' in r:
            s = r['Details']
            print(s)
        elif 'moreInformation' in r:
            s = r['moreInformation']
            print(s)
        elif 'message' in r:
            s = r['message']
            print(s)
        else:
            s = r['ErrorMessage']
            print(s)
        
    manufacturers_file = response.json()
    return manufacturers_file
        
def get_digikey_categoriesID_search(categoriesID):
    with open('digikey_token.json', 'r') as file:
        token = json.load(file)
    if token is None:
        raise Exception("No Token Loaded")
    user = get_digikey_user()
    headers = {
        'accept' : 'application/json',
        'authorization' : 'Bearer ' + token['access_token'],
        'X-DIGIKEY-Client-Id' : user['client_id'],
        'X-DIGIKEY-Locale-Site' : 'US',
        'X-DIGIKEY-Locale-Language' : 'en',
        'X-DIGIKEY-Locale-Currency' : 'USD',
        'X-DIGIKEY-Locale-ShipToCountry' : 'US' 
    }
    url = 'https://api.digikey.com/Search/v3/Categories/' + categoriesID
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        r = json.loads(response.text)
        if 'Details' in r:
            s = r['Details']
            print(s)
        elif 'moreInformation' in r:
            s = r['moreInformation']
            print(s)
        elif 'message' in r:
            s = r['message']
            print(s)
        else:
            s = r['ErrorMessage']
            print(s)
        
    categoriesID_file = response.json()
    return categoriesID_file

def get_digikey_keyword_search(key_word):
    with open('digikey_token.json', 'r') as file:
        token = json.load(file)
    if token is None:
        raise Exception("No Token Loaded")
    user = get_digikey_user()
    data = {"Keywords": key_word,
            "RecordCount": 50,
            "RecordStartPosition": 0,
            "ExcludeMarketPlaceProducts": True
           }
    headers = {
        'accept' : 'application/json',
        'authorization' : 'Bearer ' + token['access_token'],
        'X-DIGIKEY-Client-Id' : user['client_id'],
        'X-DIGIKEY-Locale-Site' : 'US',
        'X-DIGIKEY-Locale-Language' : 'en',
        'X-DIGIKEY-Locale-Currency' : 'USD',
        'X-DIGIKEY-Locale-ShipToCountry' : 'US'
    }
    url = 'https://api.digikey.com/Search/v3/Products/Keyword'

    response = requests.post(url, json=data, headers=headers) #data=json.dumps(data)
    if response.status_code != 200:
        r = json.loads(response.text)
        if 'Details' in r:
            s = r['Details']
            print(s)
        elif 'moreInformation' in r:
            s = r['moreInformation']
            print(s)
        elif 'message' in r:
            s = r['message']
            print(s)
        else:
            s = r['ErrorMessage']
            print(s)
        
    keyw_file = response.json()
    keyw_info = write_digikey_keyword_json(keyw_file)
    return keyw_file

def get_digikey_product_details_search(product_details): #SortByDigiKeyPartNumber for now
    with open('digikey_token.json', 'r') as file:
        token = json.load(file)
    if token is None:
        raise Exception("No Token Loaded")
    user = get_digikey_user()
    data = {"ManufacturerProduct": product_details,
            "RecordCount": 50,
            "RecordStartPosition": 0,
            "ExcludeMarketPlaceProducts": True
           }
    headers = {
        'accept' : 'application/json',
        'authorization' : 'Bearer ' + token['access_token'],
        'X-DIGIKEY-Client-Id' : user['client_id'],
        'X-DIGIKEY-Locale-Site' : 'US',
        'X-DIGIKEY-Locale-Language' : 'en',
        'X-DIGIKEY-Locale-Currency' : 'USD',
        'X-DIGIKEY-Locale-ShipToCountry' : 'US'
    }
    url = 'https://api.digikey.com/Search/v3/Products/ManufacturerProductDetails'
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        r = json.loads(response.text)
        if 'Details' in r:
            s = r['Details']
            print(s)
        elif 'moreInformation' in r:
            s = r['moreInformation']
            print(s)
        elif 'message' in r:
            s = r['message']
            print(s)
        else:
            s = r['ErrorMessage']
            print(s)
        
    product_file = response.json()
    return product_file
        
"""TEST CASE"""
# mfg = "MCP1501T-20E/CHY" #str(input("Please Enter Manufacture Part No.: ")); "ERJ-3EKF3901V" "571-0122-100-F"
# info = get_digikey_part_info(mfg)
# disp = display_info(info)

# sub = get_digikey_part_sub_info(mfg)
# #disp = display_sub_info(sub)

# categories = get_digikey_categories_search()

# manufacturers = get_digikey_manufacturers_search()

# categoriesID = "6" #input("Please Enter categories ID: ")
# categoriesID_file = get_digikey_categoriesID_search(categoriesID)
# #display_categoriesID_info(categoriesID_file)

# key_word = "571-0122-100-F" #"Cigarette Lighter Assemblies"
# key_result = get_digikey_keyword_search(key_word)

# product_details = "ERJ-3EKF3901V" # "TPSE476M025R0100"
# product_result = get_digikey_product_details_search(product_details)

# digikey_part = "296-27414-2-ND" # input("Please enter part #: "); "296-27414-2-ND"; "YAG5961DKR-ND"
# Qty = 1000 # input("Please enter Qty: ")
# reel_price = get_digikey_reel_pricing(digikey_part, Qty)
# print(reel_price)