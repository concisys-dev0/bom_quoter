from mouser_search_v1 import*
from mouser_search_v2 import*
import sys

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)

""""Functions to gather information from the API operation response"""
# TR3D476K025D0100, TPSE476M025R0100, RT8096AHGE, QRM8-026-07.0-L-D-A, 533980871, C0603C120J3GAC7867, MCP1501T-20E/CHY, GRM155R71H473KE14D, 06035C104K4T2A
# str(input("Please Enter Manufacture Part No.: "))
# int(input("Please Enter Qty Need: "))

# part_id = "06035C104K4T2A" 
# qty_buy = 350
# part_json = mouser_SearchByPart(part_id)

# Funtion return URL link to product
def get_url(part_json):
    if part_json['SearchResults']['NumberOfResult']!=0: # Supplier carried product
        url = part_json['SearchResults']['Parts'][0]['ProductDetailUrl']
        return url
    elif part_json['SearchResults']['NumberOfResult'] == "null": # No product exists
        return None

# Funtion return lead time of product
def get_leadtime(part_json):
    if part_json['SearchResults']['NumberOfResult']!=0: # Supplier carried product
        leadtime = part_json['SearchResults']['Parts'][0]['LeadTime']
        return leadtime
    elif part_json['SearchResults']['NumberOfResult'] == "null": # No product exists
        return None

# Funtion return amount of product in stock
def get_QOH(part_json):
    if part_json['SearchResults']['NumberOfResult']!=0: # Supplier carried product
        QOH = part_json['SearchResults']['Parts'][0]['AvailabilityInStock']
        if QOH == "0":
            if part_json['SearchResults']['Parts'][0]['Availability'] == "None": # Not in stock
                return None
        return QOH
    elif part_json['SearchResults']['NumberOfResult'] == "null": # No product exists
        return None

# Function return procduct pricing
def mouser_get_price(part_json, qty_buy):
    if part_json['SearchResults']['NumberOfResult']!=0: # Supplier carried product
        match = part_json['SearchResults']['Parts'][0] #first match product
        minimumOrder = match['PriceBreaks'][0]['Quantity'] # match['Min']
        # unitPrice = match['UnitPrice']
        counter = 0
        counter_n = 1
        max_qty = match['PriceBreaks'][-1] # last element of pricing break
        for counter in match['PriceBreaks']:
            if len(match['PriceBreaks']) <= 1: # Only 1 price
                counter_n = 0
            elif len(match['PriceBreaks']) <= counter_n:
                counter_n = len(match['PriceBreaks']) - 1 # index of last price
            value_n = match['PriceBreaks'][counter_n]['Quantity'] # Value of next quantity to compare with qty_buy
            if qty_buy < minimumOrder: # price of smallest amount can buy
                counter = 0
                unit_price = match['PriceBreaks'][counter]['Price']
                i_unit_price = float(match['PriceBreaks'][counter]['Price'].replace("$", ""))
                tt_price = i_unit_price*qty_buy
                return float(qty_buy), float(i_unit_price), float(tt_price)
            elif qty_buy >= counter['Quantity'] and qty_buy < value_n:
                unit_price = counter['Price']
                i_unit_price = float(counter['Price'].replace("$", ""))
                tt_price = i_unit_price*qty_buy
                return float(qty_buy), float(i_unit_price), float(tt_price)
            else:
                if qty_buy >= max_qty['Quantity']: # price of max amount can buy
                    unit_price = max_qty['Price']
                    i_unit_price = float(max_qty['Price'].replace("$", ""))
                    tt_price = i_unit_price*qty_buy
                    return float(qty_buy), float(i_unit_price), float(tt_price)
                counter_n += 1
                continue
    elif part_json['SearchResults']['NumberOfResult'] == "null": # No product exists
        i_unit_price = None
        tt_price = None
        return qty_buy, i_unit_price, tt_price

# def alternate_part(part_json):
#     if part_json['SearchResults']['NumberOfResult']!=0:
#         if part_json['SearchResults']['Parts'][0]['AlternatePackagings'] != None:
#             alternate_part = part_json['SearchResults']['Parts'][0]['AlternatePackagings'][0]['APMfrPN']
#             alternate_part_json = mouser_SearchByPart(alternate_part)
#             # print("Alternate manufacturer part no.:", alternate_part)
#             return alternate_part_json
#         elif part_json['SearchResults']['NumberOfResult'] == "null":
#             return None

# def get_alternate_part_price(part_json, qty_buy):
#     alternate_part_json = alternate_part(part_json)
#     if alternate_part_json != None:
#         url = get_url(alternate_part_json)
#         lead_time = get_leadtime(alternate_part_json)
#         qty_available = get_QOH(alternate_part_json)
#         pricing = get_price(alternate_part_json, qty_buy)
#     return alternate_part_json

"""TEST CASE"""
# url = get_url(part_json)
# print(url)
# qty_available = get_QOH(part_json)
# print(qty_available)
# lead_time = get_leadtime(part_json)
# print(lead_time)
# pricing = mouser_get_price(part_json, qty_buy)
# print(pricing)

# if qty_available == "0" or qty_available == "None":
#     alternate = get_alternate_part_price(part_json, qty_buy)
#     if alternate == None:
#         print("Please choose another supplier, the part and its substitute are not available")
#         sys.exit()
#     sys.exit()
