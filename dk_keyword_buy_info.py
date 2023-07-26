from bom_quoter.dk_search_info import get_digikey_keyword_search
from bom_quoter.dk_oauth2_token import*

import sys

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)

"""Functions to gather information from the API operation response"""
# str(input("Please Enter Manufacture Part No.: "))
# int(input("Please Enter Qty Need: "))
# MCP1501T-20E/CHY REG1117A C0603C120J3GAC7867 ACASA1003S1003P100 RC0603FR-077K68L C0603C0G500-220JNP AD1939YSTZ RT8096AHGE  C0402C104K4RACTU 

# Function return exact match procduct pricing
def get_price_exact(info_json, qty_buy):
    if info_json['ExactManufacturerProductsCount'] != 0: # exact match exists
        exact_match = info_json['ExactManufacturerProducts'][0] # first element
        minimumOrder = exact_match['MinimumOrderQuantity']
        unitPrice = exact_match['UnitPrice']
        if len(exact_match['StandardPricing']) == 0: # no pricing break
            max_qty = 0
            p_counter = 0 # match product start index
            # Function return match procduct pricing
            product_pricing = get_price_products(info_json, qty_buy, p_counter)
            unit_price = product_pricing[1]
            price = product_pricing[2]
            if product_pricing[1] == None and product_pricing[2]== None: # no pricing 
                unit_price = None
                price = None
                return float(qty_buy), unit_price, price 
            return float(qty_buy), float(unit_price), float(price)   
        else:
            max_qty = exact_match['StandardPricing'][-1] # last element of pricing list
        counter = 0
        count_n = 1
        for counter in exact_match['StandardPricing']:
            if len(exact_match['StandardPricing']) <= 1: # only 1 pricing break
                count_n = 0
            elif len(exact_match['StandardPricing']) <= count_n: # more than 1 price break
                counter_n = len(exact_match['StandardPricing']) - 1 # index of last price
            value_n = exact_match['StandardPricing'][count_n]['BreakQuantity']
            if qty_buy <= minimumOrder: # price of smallest amount can buy
                if len(info_json['Products']) == 1:
                    unit_price = counter['UnitPrice']
                    tt_price = counter['TotalPrice']
                    access_buy = qty_buy - counter['BreakQuantity']
                    price_ex = access_buy*unit_price
                    price = tt_price + price_ex
                    return float(qty_buy), float(unit_price), float(price)
                
                p_counter = 1 # it has exact match, start from second elements
                product_pricing = get_price_products(info_json, qty_buy, p_counter)
                unit_price = product_pricing[1]
                price = product_pricing[2]
                return float(qty_buy), float(unit_price), float(price)
            elif qty_buy >= counter['BreakQuantity'] and qty_buy < value_n:
                unit_price = counter['UnitPrice']
                tt_price = counter['TotalPrice']
                
                access_buy = qty_buy - counter['BreakQuantity']
                price_ex = access_buy*unit_price
                price = tt_price + price_ex
                return float(qty_buy), float(unit_price), float(price)
            else:
                if qty_buy >= max_qty['BreakQuantity']: # price of max amount can buy
                    unit_price = max_qty['UnitPrice']
                    tt_price = max_qty['TotalPrice']
                    access_buy = qty_buy - max_qty['BreakQuantity']
                    price_ex = access_buy*unit_price
                    price = tt_price + price_ex
                    return float(qty_buy), float(unit_price), float(price)
                count_n += 1
                continue
    elif info_json['ProductsCount'] != 0: # match product exists and no exact match
        p_counter = 0 # it doesn't have exact match
        # Function return match procduct pricing
        product_pricing = get_price_products(info_json, qty_buy, p_counter)
        unit_price = product_pricing[1]
        price = product_pricing[2]
        return float(qty_buy), float(unit_price), float(price)
    else: # error occurs
        if 'ErrorMessage' in info_json:
            print(info_json['ErrorMessage'])
            unit_price = None
            price = None
            return qty_buy, unit_price, price
        unit_price = None
        price = None
        return qty_buy, unit_price, price

# Function return match procduct pricing
def get_price_products(info_json, qty_buy, counter):
    if info_json['ProductsCount'] != 0: # match product exists 
        product_count = len(info_json['Products']) # number of match product exists 
        for p_counter in range(product_count):
            p_counter = counter # correct order path when minimum quantity lower than standard
            product = info_json['Products'][p_counter]
            mini_order = product['MinimumOrderQuantity']
            p_unit_price = product['UnitPrice']
            if len(product['StandardPricing']) == 0: # no pricing
                qty_buy = None
                unit_price = None
                price = None
                return qty_buy, unit_price, price
            else:
                max_order = product['StandardPricing'][-1] # last element of pricing list
                count = 0
                count_i = 1
                for count in product['StandardPricing']:
                    if len(product['StandardPricing']) <= 1: # only 1 pricing break
                        count_i = 0
                    val_i = product['StandardPricing'][count_i]['BreakQuantity']
                    if qty_buy < mini_order: # price of smallest amount can buy
                        unit_price = count['UnitPrice']
                        tt_price = count['TotalPrice']
                        access_buy = qty_buy - count['BreakQuantity']
                        price_ext = access_buy*unit_price
                        price = tt_price + price_ext
                        return float(qty_buy), float(unit_price), float(price)
                    elif qty_buy >= count['BreakQuantity'] and qty_buy < val_i:
                        unit_price = count['UnitPrice']
                        tt_price = count['TotalPrice']
                        access_buy = qty_buy - count['BreakQuantity']
                        price_ext = access_buy*unit_price
                        price = tt_price + price_ext
                        return float(qty_buy), float(unit_price), float(price)
                    else:
                        if qty_buy >= max_order['BreakQuantity']: # price of max amount can buy
                            unit_price = max_order['UnitPrice']
                            tt_price = max_order['TotalPrice']
                            access_buy = qty_buy - max_order['BreakQuantity']
                            price_ext = access_buy*unit_price
                            price = tt_price + price_ext
                            return float(qty_buy), float(unit_price), float(price)
                        count_i += 1
                        continue
    else: # error occurs
        if 'ErrorMessage' in info_json:
            print(info_json['ErrorMessage'])
            unit_price = None
            price = None
            return qty_buy, unit_price, price
        unit_price = None
        price = None
        return qty_buy, unit_price, price

# Funtion return URL link to product
def get_url(info_json):
    if info_json['ExactManufacturerProductsCount'] != 0: # exact match exists
        url = info_json['ExactManufacturerProducts'][0]['ProductUrl']
        return url
    elif info_json['ProductsCount'] != 0: # match product exists and no exact match
        url = info_json['Products'][0]['ProductUrl']
        return url
    else: # error occurs
        if 'ErrorMessage' in info_json:
            print(info_json['ErrorMessage'])
            return None

# Funtion return lead time of product
def get_leadtime(info_json):
    if info_json['ExactManufacturerProductsCount'] != 0: # exact match exists
        leadtime = info_json['ExactManufacturerProducts'][0]['ManufacturerLeadWeeks']
        return leadtime
    elif info_json['ProductsCount'] != 0: # match product exists and no exact match
        leadtime = info_json['Products'][0]['ManufacturerLeadWeeks']
        return leadtime
    else: # error occurs
        if 'ErrorMessage' in info_json:
            print(info_json['ErrorMessage'])
            return None

# Funtion return amount in stock of product
def get_QOH(info_json):
    if (info_json['ExactManufacturerProductsCount'] != 0): # exact match exists
        if info_json['ExactManufacturerProducts'][0]['NonStock'] == True: # product need to request
            return None
        QOH = info_json['ExactManufacturerProducts'][0]['QuantityAvailable']
        return QOH
    elif info_json['ProductsCount'] != 0: # match product exists and no exact match
        if info_json['Products'][0]['NonStock'] == True: # product need to request
            return None
        QOH = info_json['Products'][0]['QuantityAvailable']
        return QOH
    else: # error occurs
        if 'ErrorMessage' in info_json:
            print(info_json['ErrorMessage'])
            return None

# Funtion return mounting type and package/casing of product
def get_case_mountingType(info_json):
    if (info_json['ExactManufacturerProductsCount']!=0): # exact match exists
        for i in info_json['ExactManufacturerProducts'][0]['Parameters']:
            if i['Parameter'] == "Package / Case": # package/casing is available
                case = i['Value']
                break
            elif "Package / Case" in info_json: 
                case = None
                break
            else:
                case = None
                continue
        
        for n in info_json['ExactManufacturerProducts'][0]['Parameters']:
            if n['Parameter'] == "Mounting Type": # mounting type is available
                mountType = n['Value']
                break
            else:
                mountType = None
                continue
        return case, mountType
    elif info_json['ProductsCount'] != 0: # match product exists and no exact match
        for i in info_json['Products'][0]['Parameters']:
            if i['Parameter'] == "Package / Case":
                case = i['Value']
                break
            elif "Package / Case" in info_json: 
                case = None
                break
            else:
                case = None
                continue
        
        for n in info_json['Products'][0]['Parameters']:
            if n['Parameter'] == "Mounting Type":
                mountType = n['Value']
                break
            else:
                mountType = None
                continue
        return case, mountType
    else: # error occurs
        if 'ErrorMessage' in info_json:
            print(info_json['ErrorMessage'])
            return None, None
        return None, None

# Function return number of terminals of product
def get_number_terminations(info_json):
    if (info_json['ExactManufacturerProductsCount']!=0): # exact match exists
        for i in info_json['ExactManufacturerProducts'][0]['Parameters']:
            if i['Parameter'] == "Number of Pins":
                n_pin = i['Value']
                break
            elif i['Parameter'] == "Number of Terminations":
                n_pin = i['Value']
                break
            else:
                n_pin = None
                continue
        return n_pin
    elif info_json['ProductsCount'] != 0: # match product exists and no exact match
        for i in info_json['Products'][0]['Parameters']:
            if i['Parameter'] == "Number of Pins":
                n_pin = i['Value']
                break
            elif i['Parameter'] == "Number of Terminations":
                n_pin = i['Value']
                break
            else:
                n_pin = None
                continue
        return n_pin
    else: # error occurs
        if 'ErrorMessage' in info_json:
            print(info_json['ErrorMessage'])
            return None
        return None

"""TEST CASE"""
# part_id = "AD1939YSTZ"
# qty_buy = 75
# info_json = get_digikey_keyword_search(part_id)
# if 'ErrorMessage' in info_json:
#     refresh_token_digikey_api()
#     info_json = get_digikey_keyword_search(part_id)

# url = get_url(info_json)
# print(url)
# qty_available = get_QOH(info_json)
# print(qty_available)

# pricing = get_price_exact(info_json, qty_buy)
# print(pricing)

# lead_time = get_leadtime(info_json)
# print(lead_time)
# case_mounting = get_case_mountingType(info_json)
# print(case_mounting)
# pin = get_number_terminations(info_json)
# print(pin)