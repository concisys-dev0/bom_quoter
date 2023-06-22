from mouser_search_v1 import*
from mouser_search_v2 import*

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)

import sys

# part_id = "06035C104K4T2A" 
# str(input("Please Enter Manufacture Part No.: "))
# qty_buy = 350
# int(input("Please Enter Qty Need: "))
# part_json = mouser_SearchByPart(part_id)

def get_url(part_json):
    if part_json['SearchResults']['NumberOfResult']!=0:
        url = part_json['SearchResults']['Parts'][0]['ProductDetailUrl']
        # print(" ".join (["Product Url:", str(url)]))
        return url
    elif part_json['SearchResults']['NumberOfResult'] == "null":
        return None

def get_leadtime(part_json):
    if part_json['SearchResults']['NumberOfResult']!=0:
        leadtime = part_json['SearchResults']['Parts'][0]['LeadTime']
        # print(" ".join (["Lead time:", str(leadtime)]))
        return leadtime
    elif part_json['SearchResults']['NumberOfResult'] == "null":
        return None

def get_QOH(part_json):
    if part_json['SearchResults']['NumberOfResult']!=0:
        QOH = part_json['SearchResults']['Parts'][0]['AvailabilityInStock']
        if QOH == "0":
            if part_json['SearchResults']['Parts'][0]['Availability'] == "None":
                return None
        # print(" ".join (["Quantity available:", str(QOH)]))
        return QOH
    elif part_json['SearchResults']['NumberOfResult'] == "null":
        return None

def mouser_get_price(part_json, qty_buy):
    if part_json['SearchResults']['NumberOfResult']!=0:
        match = part_json['SearchResults']['Parts'][0]
        minimumOrder = match['PriceBreaks'][0]['Quantity'] # match['Min']
        # print(minimumOrder)
        # unitPrice = match['UnitPrice']
        counter = 0
        counter_n = 1
        max_qty = match['PriceBreaks'][-1]
        for counter in match['PriceBreaks']:
            if len(match['PriceBreaks']) <= 1:
                counter_n = 0
            elif len(match['PriceBreaks']) <= counter_n:
                counter_n = len(match['PriceBreaks'])
            value_n = match['PriceBreaks'][counter_n]['Quantity']
            if qty_buy < minimumOrder:
                counter = 0
                unit_price = match['PriceBreaks'][counter]['Price']
                i_unit_price = float(match['PriceBreaks'][counter]['Price'].replace("$", ""))
                tt_price = i_unit_price*qty_buy
                # print(" ".join (["Break Quantity:", str(counter['Quantity']),"; Unit price:", str(unit_price)]))
                # print(" ".join (["Quantity buy:", str(qty_buy),"; Unit price:", str(unit_price), "; Total price:", str(tt_price)]))
                return float(qty_buy), float(i_unit_price), float(tt_price)
            elif qty_buy >= counter['Quantity'] and qty_buy < value_n:
                unit_price = counter['Price']
                i_unit_price = float(counter['Price'].replace("$", ""))
                tt_price = i_unit_price*qty_buy
                # print(" ".join (["Break Quantity:", str(counter['Quantity']),"; Unit price:", str(unit_price)]))
                # print(" ".join (["Quantity buy:", str(qty_buy),"; Unit price:", str(unit_price), "; Total price:", str(tt_price)]))
                return float(qty_buy), float(i_unit_price), float(tt_price)
            else:
                if qty_buy >= max_qty['Quantity']:
                    unit_price = max_qty['Price']
                    i_unit_price = float(max_qty['Price'].replace("$", ""))
                    tt_price = i_unit_price*qty_buy
                    # print(" ".join (["Break Quantity:", str(max_qty['Quantity']),"; Unit price:", str(unit_price)]))
                    # print(" ".join (["Quantity buy:", str(qty_buy),"; Unit price:", str(unit_price), "; Total price:", str(tt_price)]))
                    return float(qty_buy), float(i_unit_price), float(tt_price)
                counter_n += 1
                continue
    elif part_json['SearchResults']['NumberOfResult'] == "null":
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

# TR3D476K025D0100, TPSE476M025R0100, RT8096AHGE, QRM8-026-07.0-L-D-A, 533980871, C0603C120J3GAC7867, MCP1501T-20E/CHY, GRM155R71H473KE14D, 06035C104K4T2A