import os
import sys
import re
import requests
import json

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)

apiKey = "a0eeffff-84b7-41a7-91a4-3a898603a969"
ver1 = "v1"

# def write_mouser_keyword_json(keyword_file):
#     access_file = 'mouser_keyword_info.json'
#     with open(access_file, 'w') as file:
#         json.dump(keyword_file, file, indent=4)
        
def write_mouser_part_json(part_file):
    access_file = 'mouser_part_info.json'
    with open(access_file, 'w') as file:
        json.dump(part_file, file, indent=4)
        
def mouser_SearchByKeyword(keyword):
    request = {"SearchByKeywordRequest": 
               {"keyword": keyword,
                "records": 50,
                "startingRecord": 0,
                "searchOptions": "string",
                "searchWithYourSignUpLanguage": "English"}
              } #body
    headers = {
        'accept' : 'application/json',
        'Content-Type' : 'application/json'
    }
    url = "https://api.mouser.com/api/"+ ver1 + "/search/keyword?apiKey=" + apiKey
    response = requests.post(url, json=request, headers=headers)
    if response.status_code != 200:
        r = json.loads(response.text)
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
    # keyword_info = write_mouser_keyword_json(keyword_file)
    # print(response.status_code)
    return keyword_file

def mouser_SearchByPart(part_id):
    request = {"SearchByPartRequest": 
               {"mouserPartNumber": part_id,
                "partSearchOptions": "string"}
              } #body
    headers = {
        'accept' : 'application/json',
        'Content-Type' : 'application/json'
    }
    url = "https://api.mouser.com/api/"+ ver1 + "/search/partnumber?apiKey=" + apiKey
    response = requests.post(url, json=request, headers=headers)
    if response.status_code != 200:
        r = json.loads(response.text)
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
            s = r['Errors'][0]['Message']
        # raise Exception(s)
        
    part_file = response.json()
    part_info = write_mouser_part_json(part_file)
    # print(response.status_code)
    return part_file

"""TEST CASE"""
# keyword = "TPS54240DGQR" # "1397878-1" "H00040557_REV01"
# searchKeyword = mouser_SearchByKeyword(keyword)

# part_id = "0533980871" # "ABM8-12.000MHZ-B2-T"
# searchPart = mouser_SearchByPart(part_id)
