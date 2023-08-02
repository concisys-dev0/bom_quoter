import requests
import json
import sys
import os

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)

from utils.dk_oauth2_token import *
from utils.constants import DK_TOKEN_STORAGE, DK_RESULTS_STORAGE

"""API operations related to product information: part search"""

# def write_digikey_part_info(info_file):
#     access_file = 'digikey_part_info.json'
#     with open(access_file, 'w') as fil:
#         json.dump(info_file, fil, indent=4)
        
# def write_digikey_sub_json(sub_file):
#     access_file = 'digikey_sub_info.json'
#     with open(access_file, 'w') as fil:
#         json.dump(sub_file, fil, indent=4)

# def write_digikey_categories_json(categories_file):
#     access_file = 'digikey_categories_info.json'
#     with open(access_file, 'w') as file:
#         json.dump(categories_file, file, indent=4)
        
# def write_digikey_manufacturers_json(manufacturers_file):
#     access_file = 'digikey_manufacturers_info.json'
#     with open(access_file, 'w') as file:
#         json.dump(manufacturers_file, file, indent=4)
        
# def write_digikey_categoriesID_json(categoriesID_file):
#     access_file = 'digikey_categoriesID_info.json'
#     with open(access_file, 'w') as file:
#         json.dump(categoriesID_file, file, indent=4)
        
# def write_digikey_keyword_json(keyword_file):
#     access_file = 'digikey_keyword_info.json'
#     with open(access_file, 'w') as fil:
#         json.dump(keyword_file, fil, indent=4)
        
# def write_digikey_product_details_json(product_file):
#     access_file = 'digikey_product_details_info.json'
#     with open(access_file, 'w') as fil:
#         json.dump(product_file, fil, indent=4)

# Retrieve detailed product information including real time pricing and availability.
def get_digikey_part_info(part_id):
    with open(DK_TOKEN_STORAGE, 'r') as file: # to get access token
        token = json.load(file)
    if token['access_token'] is None:
        raise Exception("No Token Loaded")
    user = get_digikey_user() # to get client id
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
    # + quote(part_id, safe='')
    # Config().log_write("Query " + part_id + " with token " + Config().access_token_string)
    response = requests.get(url, headers=headers, verify=False) #, timeout=10
    # Config().log_write("Response Code " + str(response.status_code))
    if response.status_code != 200: # HTTP connection error
        r = json.loads(response.text)
        # print error message
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
    # part_info = write_digikey_part_info(info_file) # save response info
    return info_file

# Retrieve detailed product information and two suggested products. 
def get_digikey_part_sub_info(part_id):
    with open(DK_TOKEN_STORAGE, 'r') as file: # to get access token
        token = json.load(file)
    if token['access_token'] is None:
        raise Exception("No Token Loaded")
    user = get_digikey_user() # to get client id
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
    response = requests.get(url, headers=headers, verify=False) #, timeout=10
    if response.status_code != 200: # HTTP connection error
        r = json.loads(response.text)
        # print error message
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
    # sub_info = write_digikey_sub_json(sub_file) # save response info
    return sub_file

# Calculate the DigiReel pricing for the given DigiKeyPartNumber and RequestedQuantity
def get_digikey_reel_pricing(digikey_part, Qty):
    with open(DK_TOKEN_STORAGE, 'r') as file: # to get access token
        token = json.load(file)
    if token['access_token'] is None:
        raise Exception("No Token Loaded")
    user = get_digikey_user() # to get client id
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
    response = requests.get(url, params=params, headers=headers, verify=False) #, timeout=10
    if response.status_code != 200: # HTTP connection error
        r = json.loads(response.text)
        # print error message
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

# Returns all Product Categories. Category Id can be used in KeywordSearchRequest.Filters.TaxonomyIds to restrict a keyword search to a given category
def get_digikey_categories_search():
    with open(DK_TOKEN_STORAGE, 'r') as file: # to get access token
        token = json.load(file)
    if token is None:
        raise Exception("No Token Loaded")
    user = get_digikey_user() # to get client id
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
    response = requests.get(url, headers=headers, verify=False) #, timeout=10
    if response.status_code != 200: # HTTP connection error
        r = json.loads(response.text)
        # print error message
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
    # categories_list = write_digikey_categories_json(categories_file) # save response info
    return categories_file

# Returns all Product Manufacturers. ManufacturersId can be used in KeywordSearchRequest.Filters.ManufacturerIds to restrict a keyword search to a given Manufacturer
def get_digikey_manufacturers_search():
    with open(DK_TOKEN_STORAGE, 'r') as file: # to get access token
        token = json.load(file)
    if token is None:
        raise Exception("No Token Loaded")
    user = get_digikey_user() # to get client id
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
    response = requests.get(url, headers=headers, verify=False) #, timeout=10
    if response.status_code != 200: # HTTP connection error
        r = json.loads(response.text)
        # print error message
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
    # manufacturers_list = write_digikey_manufacturers_json(manufacturers_file) # save response info
    return manufacturers_file

# Returns Category for given Id. Category Id can be used in KeywordSearchRequest.Filters.TaxonomyIds to restrict a keyword search to a given category
def get_digikey_categoriesID_search(categoriesID):
    with open(DK_TOKEN_STORAGE, 'r') as file: # to get access token
        token = json.load(file)
    if token is None:
        raise Exception("No Token Loaded")
    user = get_digikey_user() # to get client id
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
    response = requests.get(url, headers=headers, verify=False) #, timeout=10
    if response.status_code != 200: # HTTP connection error
        r = json.loads(response.text)
        # print error message
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
    # categoriesID_list = write_digikey_categoriesID_json(categoriesID_file) # save response info
    return categoriesID_file

# KeywordSearch can search for any product in the Digi-Key catalog.
def get_digikey_keyword_search(key_word):
    with open(DK_TOKEN_STORAGE, 'r') as file: # to get access token
        token = json.load(file)
    if token is None:
        raise Exception("No Token Loaded")
    user = get_digikey_user() # to get client id
    data = {"Keywords": key_word,
            "RecordCount": 50,
            "RecordStartPosition": 0,
            "ExcludeMarketPlaceProducts": True
           }
    headers = {
        'accept' : 'application/json',
        'authorization' : 'Bearer ' + token['access_token'],
        'X-DIGIKEY-Client-Id' : user['client_id'], # user
        'X-DIGIKEY-Locale-Site' : 'US',
        'X-DIGIKEY-Locale-Language' : 'en',
        'X-DIGIKEY-Locale-Currency' : 'USD',
        'X-DIGIKEY-Locale-ShipToCountry' : 'US'
    }
    url = 'https://api.digikey.com/Search/v3/Products/Keyword'

    response = requests.post(url, json=data, headers=headers, verify=False) #data=json.dumps(data), timeout=10
    if response.status_code != 200: # HTTP connection error
        r = json.loads(response.text)
        # print error message
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
    # print(response.headers) # Debug
    keyw_file = response.json()
    # keyw_info = write_digikey_keyword_json(keyw_file) # save response info
    return keyw_file

# Create list of ProductDetails from the matches of the requested manufacturer product name.
def get_digikey_product_details_search(product_details): #SortByDigiKeyPartNumber for now
    with open(DK_TOKEN_STORAGE, 'r') as file: # to get access token
        token = json.load(file)
    if token is None:
        raise Exception("No Token Loaded")
    user = get_digikey_user() # to get client
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
    response = requests.post(url, json=data, headers=headers, verify=False) #, timeout=10
    # if response.status_code != 200:
    #     r = json.loads(response.text)
    #     if 'Details' in r:
    #         print(response.status_code)
    #         s = r['Details']
    #     elif 'moreInformation' in r:
    #         print(response.status_code)
    #         s = r['moreInformation']
    #     elif 'message' in r:
    #         print(response.status_code)
    #         s = r['message']
    #     else:
    #         print(response.status_code)
    #         s = r['ErrorMessage']
    #     raise Exception(s)
    if response.status_code != 200: # HTTP connection error
        r = json.loads(response.text)
        # print error message
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
    # product_info = write_digikey_product_details_json(product_file) # save response info
    # print(response.status_code)
    return product_file

"""TEST CASE"""
# mfg = "MCP1501T-20E/CHY" #str(input("Please Enter Manufacture Part No.: ")); "ERJ-3EKF3901V" "571-0122-100-F"
# info = get_digikey_part_info(mfg)

# sub = get_digikey_part_sub_info(mfg)

# categories = get_digikey_categories_search()

# manufacturers = get_digikey_manufacturers_search()

# categoriesID = "6" #input("Please Enter categories ID: ")
# categoriesID_file = get_digikey_categoriesID_search(categoriesID)

# key_word = "571-0122-100-F" #"Cigarette Lighter Assemblies"
# key_result = get_digikey_keyword_search(key_word)

# product_details = "ERJ-3EKF3901V" # "TPSE476M025R0100"
# product_result = get_digikey_product_details_search(product_details)

# digikey_part = "296-27414-2-ND" # input("Please enter part #: "); "296-27414-2-ND"; "YAG5961DKR-ND"
# Qty = 1000 # input("Please enter Qty: ")
# reel_price = get_digikey_reel_pricing(digikey_part, Qty)
# print(reel_price)