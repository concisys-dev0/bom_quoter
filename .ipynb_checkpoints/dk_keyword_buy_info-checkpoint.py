from dk_search_info import get_digikey_keyword_search
from dk_oauth2_token import*

import sys

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)

# part_id = "RC0603FR-077K68L"
# str(input("Please Enter Manufacture Part No.: ")) MCP1501T-20E/CHY REG1117A C0603C120J3GAC7867 ACASA1003S1003P100
# qty_buy = 100
# int(input("Please Enter Qty Need: "))

# info_json = get_digikey_keyword_search(part_id)
# if 'ErrorMessage' in info_json:
#     refresh_token_digikey_api()
#     info_json = get_digikey_keyword_search(part_id)
    
def get_price_exact(info_json, qty_buy):
    if info_json['ExactManufacturerProductsCount'] != 0:
        exact_match = info_json['ExactManufacturerProducts'][0]
        minimumOrder = exact_match['MinimumOrderQuantity']
        unitPrice = exact_match['UnitPrice']
        # print(" ".join (["Minimum order quantity:", str(minimumOrder), "Unit price:", str(unitPrice)]))
        if len(exact_match['StandardPricing']) == 0:
            max_qty = 0
            p_counter = 0 #if it doesn't have exact match
            product_pricing = get_price_products(info_json, qty_buy, p_counter)
            unit_price = product_pricing[1]
            price = product_pricing[2]
            return float(qty_buy), float(unit_price), float(price)
            
        else:
            max_qty = exact_match['StandardPricing'][-1]
        counter = 0
        count_n = 1
        for counter in exact_match['StandardPricing']:
            if len(exact_match['StandardPricing']) <= 1:
                count_n = 0
            value_n = exact_match['StandardPricing'][count_n]['BreakQuantity']
            if qty_buy < minimumOrder:
                if len(info_json['Products']) == 1:
                    unit_price = counter['UnitPrice']
                    tt_price = counter['TotalPrice']
                    # print(" ".join (["Break Quantity:", str(counter['BreakQuantity']),"; Unit price:", str(unit_price), "; Total price:", str(tt_price)]))
                    access_buy = qty_buy - counter['BreakQuantity']
                    price_ex = access_buy*unit_price
                    price = tt_price + price_ex
                    # print(" ".join (["Qty buy:", str(qty_buy), "; Price:", str(price)]))
                    return float(qty_buy), float(unit_price), float(price)
                
                p_counter = 1 #if it has exact match, start from second elements
                product_pricing = get_price_products(info_json, qty_buy, p_counter)
                unit_price = product_pricing[1]
                price = product_pricing[2]
                return float(qty_buy), float(unit_price), float(price)
            elif qty_buy >= counter['BreakQuantity'] and qty_buy < value_n:
                unit_price = counter['UnitPrice']
                tt_price = counter['TotalPrice']
                # print(" ".join (["Break Quantity:", str(counter['BreakQuantity']),"; Unit price:", str(unit_price), "; Total price:", str(tt_price)]))
                access_buy = qty_buy - counter['BreakQuantity']
                price_ex = access_buy*unit_price
                price = tt_price + price_ex
                # print(" ".join (["Qty buy:", str(qty_buy), "; Price:", str(price)]))
                return float(qty_buy), float(unit_price), float(price)
            else:
                if qty_buy >= max_qty['BreakQuantity'] :
                    unit_price = max_qty['UnitPrice']
                    tt_price = max_qty['TotalPrice']
                    # print(" ".join (["Break Quantity:", str(max_qty['BreakQuantity']),"; Unit price:", str(unit_price), "; Total price:", str(tt_price)]))
                    access_buy = qty_buy - max_qty['BreakQuantity']
                    price_ex = access_buy*unit_price
                    price = tt_price + price_ex
                    # print(" ".join (["Qty buy:", str(qty_buy), "; Price:", str(price)]))
                    return float(qty_buy), float(unit_price), float(price)
                count_n += 1
                continue
    elif info_json['ProductsCount'] != 0:
        p_counter = 0 #if it doesn't have exact match
        product_pricing = get_price_products(info_json, qty_buy, p_counter)
        unit_price = product_pricing[1]
        price = product_pricing[2]
        return float(qty_buy), float(unit_price), float(price)
    else:
        if 'ErrorMessage' in info_json:
            print(info_json['ErrorMessage'])
            unit_price = None
            price = None
            return qty_buy, unit_price, price
        unit_price = None
        price = None
        return qty_buy, unit_price, price

def get_price_products(info_json, qty_buy, p_counter):
    if info_json['ProductsCount'] != 0:
        product_count = len(info_json['Products'])
        for p_counter in range(product_count):
            product = info_json['Products'][p_counter]
            mini_order = product['MinimumOrderQuantity']
            p_unit_price = product['UnitPrice']
            if len(product['StandardPricing']) == 0:
                qty_buy = None
                unit_price = None
                price = None
                continue
            else:
                max_order = product['StandardPricing'][-1]
                # print(max_order)
                count = 0
                count_i = 1
                for count in product['StandardPricing']:
                    if len(product['StandardPricing']) <= 1:
                        count_i = 0
                    val_i = product['StandardPricing'][count_i]['BreakQuantity']
                    if qty_buy <= mini_order:
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
                        if qty_buy >= max_order['BreakQuantity']:
                            unit_price = max_order['UnitPrice']
                            tt_price = max_order['TotalPrice']
                            access_buy = qty_buy - max_order['BreakQuantity']
                            price_ext = access_buy*unit_price
                            price = tt_price + price_ext
                            return float(qty_buy), float(unit_price), float(price)
                        count_i += 1
                        continue
    else:
        if 'ErrorMessage' in info_json:
            print(info_json['ErrorMessage'])
            unit_price = None
            price = None
            return qty_buy, unit_price, price
        unit_price = None
        price = None
        return qty_buy, unit_price, price

def get_url(info_json):
    if info_json['ExactManufacturerProductsCount'] != 0:
        url = info_json['ExactManufacturerProducts'][0]['ProductUrl']
        # print(" ".join (["Product Url:", url]))
        return url
    elif info_json['ProductsCount'] != 0:
        url = info_json['Products'][0]['ProductUrl']
        # print(" ".join (["Product Url:", url]))
        return url
    else:
        if 'ErrorMessage' in info_json:
            print(info_json['ErrorMessage'])
            return None
        # print("Cannot Found")

def get_leadtime(info_json):
    if info_json['ExactManufacturerProductsCount'] != 0:
        leadtime = info_json['ExactManufacturerProducts'][0]['ManufacturerLeadWeeks']
        # print(" ".join (["Lead time:", leadtime]))
        return leadtime
    elif info_json['ProductsCount'] != 0:
        leadtime = info_json['Products'][0]['ManufacturerLeadWeeks']
        # print(" ".join (["Lead time:", leadtime]))
        return leadtime
    else:
        if 'ErrorMessage' in info_json:
            print(info_json['ErrorMessage'])
            return None
        # print("Cannot Found")
        
def get_QOH(info_json):
    if (info_json['ExactManufacturerProductsCount'] != 0):
        if info_json['ExactManufacturerProducts'][0]['NonStock'] == True:
            return None
        QOH = info_json['ExactManufacturerProducts'][0]['QuantityAvailable']
        # print(" ".join (["Quantity available:", str(QOH)]))
        return QOH
    elif info_json['ProductsCount'] != 0:
        if info_json['Products'][0]['NonStock'] == True:
            return None
        QOH = info_json['Products'][0]['QuantityAvailable']
        # print(" ".join (["Quantity available:", str(QOH)]))
        return QOH
    else:
        if 'ErrorMessage' in info_json:
            print(info_json['ErrorMessage'])
            return None
        # print("Cannot Found")
        
def get_case_mountingType(info_json):
    if (info_json['ExactManufacturerProductsCount']!=0):
        for i in info_json['ExactManufacturerProducts'][0]['Parameters']:
            if i['Parameter'] == "Package / Case":
                # print(" ".join ([i['Parameter'], ":", i['Value']]))
                case = i['Value']
                break
            elif "Package / Case" in info_json: 
                case = None
                break
            else:
                case = None
                continue
        
        for n in info_json['ExactManufacturerProducts'][0]['Parameters']:
            if n['Parameter'] == "Mounting Type":
                # print(" ".join ([n['Parameter'], ":", n['Value']]))
                mountType = n['Value']
                break
            else:
                mountType = None
                continue
        return case, mountType
    elif info_json['ProductsCount'] != 0:
        for i in info_json['Products'][0]['Parameters']:
            if i['Parameter'] == "Package / Case":
                # print(" ".join ([i['Parameter'], ":", i['Value']]))
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
                # print(" ".join ([n['Parameter'], ":", n['Value']]))
                mountType = n['Value']
                break
            else:
                mountType = None
                continue
        return case, mountType
    else:
        if 'ErrorMessage' in info_json:
            print(info_json['ErrorMessage'])
            return None, None
        return None, None
        # print("Cannot Found")

def get_number_terminations(info_json):
    if (info_json['ExactManufacturerProductsCount']!=0):
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
    elif info_json['ProductsCount'] != 0:
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

"""TEST CASE"""
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