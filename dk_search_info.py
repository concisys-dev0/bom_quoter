import requests
import json
import sys
import os

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)

client_id = 'jhZJWxD67jf2ONa8MAzE6eQAC8UtR1bM'
# tester1: 'B7oWwd6qhoswuTNKR5XNjVOJgavWhqG3'
# ldo: 'jhZJWxD67jf2ONa8MAzE6eQAC8UtR1bM' 
# excess: 'v96weKvwrkhbxsufdcrABCd7tMT4wfuj'

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
        
def write_digikey_keyword_json(keyword_file):
    access_file = 'digikey_keyword_info.json'
    with open(access_file, 'w') as fil:
        json.dump(keyword_file, fil, indent=4)
        
# def write_digikey_product_details_json(product_file):
#     access_file = 'digikey_product_details_info.json'
#     with open(access_file, 'w') as fil:
#         json.dump(product_file, fil, indent=4)
        
def get_digikey_part_info(part_id):
    with open('digikey_token.json', 'r') as file:
        token = json.load(file)
    if token['access_token'] is None:
        raise Exception("No Token Loaded")
    headers = {
        'accept' : 'application/json',
        'authorization' : 'Bearer ' + token['access_token'],
        'X-DIGIKEY-Client-Id' : client_id,
        'X-DIGIKEY-Locale-Site' : 'US',
        'X-DIGIKEY-Locale-Language' : 'en',
        'X-DIGIKEY-Locale-Currency' : 'USD',
        'X-DIGIKEY-Locale-ShipToCountry' : 'US'
    }
    url = 'https://api.digikey.com/Search/v3/Products/' + part_id
    #+ quote(part_id, safe='')
    #Config().log_write("Query " + part_id + " with token " + Config().access_token_string)
    response = requests.get(url, headers=headers)
    #Config().log_write("Response Code " + str(response.status_code))
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
    # part_info = write_digikey_part_info(info_file)
    return info_file

def get_digikey_part_sub_info(part_id):
    with open('digikey_token.json', 'r') as file:
        token = json.load(file)
    if token['access_token'] is None:
        raise Exception("No Token Loaded")
    headers = {
        'accept' : 'application/json',
        'partNumber' : part_id,
        'authorization' : 'Bearer ' + token['access_token'],
        'X-DIGIKEY-Client-Id' : client_id,
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
    # sub_info = write_digikey_sub_json(sub_file)
    return sub_file

def get_digikey_reel_pricing(digikey_part, Qty):
    with open('digikey_token.json', 'r') as file:
        token = json.load(file)
    if token['access_token'] is None:
        raise Exception("No Token Loaded")
    params = {
        'digiKeyPartNumber' : digikey_part,
        'requestedQuantity' : Qty,
        'includes' : 'ExtendedPrice,ReelingFee,UnitPrice,SearchLocaleUsed'}
    headers = {
        'accept' : 'application/json',
        'Authorization' : 'Bearer ' + token['access_token'],
        'X-DIGIKEY-Client-Id' : client_id,
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
    headers = {
        'accept' : 'application/json',
        'authorization' : 'Bearer ' + token['access_token'],
        'X-DIGIKEY-Client-Id' : client_id,
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
    # categories_list = write_digikey_categories_json(categories_file)
    return categories_file
        
def get_digikey_manufacturers_search():
    with open('digikey_token.json', 'r') as file:
        token = json.load(file)
    if token is None:
        raise Exception("No Token Loaded")
    headers = {
        'accept' : 'application/json',
        'authorization' : 'Bearer ' + token['access_token'],
        'X-DIGIKEY-Client-Id' : client_id,
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
    # manufacturers_list = write_digikey_manufacturers_json(manufacturers_file)
    return manufacturers_file
        
def get_digikey_categoriesID_search(categoriesID):
    with open('digikey_token.json', 'r') as file:
        token = json.load(file)
    if token is None:
        raise Exception("No Token Loaded")
    headers = {
        'accept' : 'application/json',
        'authorization' : 'Bearer ' + token['access_token'],
        'X-DIGIKEY-Client-Id' : client_id,
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
    # categoriesID_list = write_digikey_categoriesID_json(categoriesID_file)
    return categoriesID_file

def get_digikey_keyword_search(key_word):
    with open('digikey_token.json', 'r') as file:
        token = json.load(file)
    if token is None:
        raise Exception("No Token Loaded")
        
    data = {"Keywords": key_word,
            "RecordCount": 50,
            "RecordStartPosition": 0,
            "ExcludeMarketPlaceProducts": True
           }
    headers = {
        'accept' : 'application/json',
        'authorization' : 'Bearer ' + token['access_token'],
        'X-DIGIKEY-Client-Id' : client_id,
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
        
    data = {"ManufacturerProduct": product_details,
            "RecordCount": 50,
            "RecordStartPosition": 0,
            "ExcludeMarketPlaceProducts": True
           }
    headers = {
        'accept' : 'application/json',
        'authorization' : 'Bearer ' + token['access_token'],
        'X-DIGIKEY-Client-Id' : client_id,
        'X-DIGIKEY-Locale-Site' : 'US',
        'X-DIGIKEY-Locale-Language' : 'en',
        'X-DIGIKEY-Locale-Currency' : 'USD',
        'X-DIGIKEY-Locale-ShipToCountry' : 'US'
    }
    url = 'https://api.digikey.com/Search/v3/Products/ManufacturerProductDetails'
    response = requests.post(url, json=data, headers=headers)
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
    # product_info = write_digikey_product_details_json(product_file)
    # print(response.status_code)
    return product_file

# def display_info(info_file):
#     print("Manufacturer Part Number: " + info_file["ManufacturerPartNumber"])
#     print("Digi-Key Part Number:" + info_file['DigiKeyPartNumber'])
#     print("Manufacturer: " + info_file["Manufacturer"]["Value"])
#     print("Type: " + info_file["Category"]["Value"])
#     print("Description: " + info_file["ProductDescription"])

# def display_sub_info(sub_file):
#     for sub_info in sub_file['SuggestedProducts']:
#         print("Manufacturer Part Number: " + sub_info['ManufacturerPartNumber'])
#         print("Digi-Key Part Number:" + sub_info['DigiKeyPartNumber'])
#         print("Manufacturer: " + sub_info['Manufacturer']['Value'])
#         print("Description: " + sub_info["ProductDescription"])
#         print("")

# def display_categories_info(categories_file):
#     for categories_info in categories_file['Categories']:
#         print("CategoryId: " + str(categories_info['CategoryId']))
#         print("Name: " + categories_info['Name'])
#         print("")

# def display_manufacturers_info(manufacturers_file):
#     for manufacturers_info in manufacturers_file['Manufacturers']:
#         print("Id: " + str(manufacturers_info['Id']))
#         print("Name: " + manufacturers_info['Name'])
#         print("")
        
# def display_categoriesID_info(categoriesID_file):
#     print("Name: " + categoriesID_file['Name'])
#     for categoriesID_info in categoriesID_file['Children']:
#         print("Category Id: " + str(categoriesID_info['CategoryId']))
#         print("Name: " + categoriesID_info['Name'])
#         print("Product count: " + str(categoriesID_info['ProductCount']))
#         print("")
        
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