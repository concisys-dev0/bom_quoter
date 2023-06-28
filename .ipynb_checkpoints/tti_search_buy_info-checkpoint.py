from tti_search import*

import math
import sys

import urllib3
urllib3.disable_warnings()
import logging
logging.captureWarnings(True)

# "597-5311-402F"
# "T521X476M035ATE030"
# "RC0603FR-074K99L"
# "RM222-080-211-5570"
# str(input("Please Enter Manufacture Part No.: "))
# int(input("Please Enter Qty Need: "))

# part_id = "5001"
# qty_buy = 210
# info_json = tti_SearchByKeyword(part_id)
# if 'recordCount' in info_json and info_json['recordCount'] == 0:
#     print("The part is not available please try another supplier. ")
#     sys.exit()
# elif 'code' in info_json:
#     print(info_json['code'] + ": " + info_json['message'])
#     sys.exit()

def get_url(info_json):
    if info_json['parts']!=0:
        url = info_json['parts'][0]['buyUrl']
        # print(" ".join (["URL:", str(url)]))
        return url
    else:
        if 'code' in info_json:
            # print(info_json['code'] + ": " + info_json['message'])
            return None
        url = None
        return url

def get_QOH(info_json):
    if info_json['parts']!=0:
        QOH = info_json['parts'][0]['availableToSell']
        # print(" ".join (["Quantity available:", str(QOH)]))
        return QOH
    else:
        if 'code' in info_json:
            print(info_json['code'] + ": " + info_json['message'])
            return None
        QOH = None
        return QOH

def get_leadtime(info_json):
    if info_json['parts']!=0:
        leadtime = info_json['parts'][0]['leadTime']
        # print(" ".join (["Lead time:", str(leadtime)]))
        return leadtime
    else:
        if 'code' in info_json:
            print(info_json['code'] + ": " + info_json['message'])
            return None
        leadtime = None
        return leadtime

def get_case_mountingType(info_json):
    if info_json['parts']!=0:
        if 'case' in info_json['parts'][0]:
            case = info_json['parts'][0]['case']
            # print(" ".join (["Package/Case:", str(case)]))
        else: 
            case = None
        return case
    else:
        if 'code' in info_json:
            print(info_json['code'] + ": " + info_json['message'])
            return None
        return None

def get_price(info_json, qty_buy):
    qty_available = get_QOH(info_json)
    if qty_available == 0:
        unit_price = None
        tt_price = None
        return qty_buy, unit_price, tt_price
    
    if info_json['parts']!=0:
        match = info_json['parts'][0]
        minimumOrder = match['salesMinimum']
        if minimumOrder < match['pricing']['quantityPriceBreaks'][0]['quantity']:
            minimumOrder = match['pricing']['quantityPriceBreaks'][0]['quantity']
        sale_by = match['salesMultiple']
        counter = 0
        counter_n = 1
        if len(match['pricing']) == 0:
            unit_price = None
            tt_price = None
            return qty_buy, unit_price, tt_price
        max_qty = match['pricing']['quantityPriceBreaks'][-1]
        for counter in match['pricing']['quantityPriceBreaks']:
            if len(match['pricing']['quantityPriceBreaks']) <= 1:
                counter_n = 0
            elif len(match['pricing']['quantityPriceBreaks']) <= counter_n:
                counter_n = len(match['pricing']['quantityPriceBreaks'])-1
            value_n = match['pricing']['quantityPriceBreaks'][counter_n]['quantity']
            if qty_buy <= minimumOrder:
                qty_buy = minimumOrder
                unit_price = float(match['pricing']['quantityPriceBreaks'][0]['price'])
                tt_price = unit_price*minimumOrder
                return qty_buy, unit_price, tt_price
            elif qty_buy >= counter['quantity'] and qty_buy < value_n:
                unit_price = float(counter['price'])
                sur_plus = qty_buy - counter['quantity']
                if sur_plus <= sale_by:
                    tt_price = (unit_price*counter['quantity']) + (unit_price*sale_by)
                    return qty_buy, unit_price, tt_price
                elif sur_plus > sale_by:
                    mult = math.ceil(sur_plus/sale_by)
                    tt_price = (unit_price*counter['quantity']) + (unit_price*(sale_by*mult))
                return qty_buy, unit_price, tt_price
            elif qty_buy >= max_qty['quantity']:
                unit_price = float(max_qty['price'])
                sur_plus = qty_buy - max_qty['quantity']
                if sur_plus <= sale_by:
                    tt_price = (unit_price*max_qty['quantity']) + (unit_price*sale_by)
                    return qty_buy, unit_price, tt_price
                elif sur_plus > sale_by:
                    mult = math.ceil(sur_plus/sale_by)
                    tt_price = (unit_price*max_qty['quantity']) + (unit_price*(sale_by*mult))
                    return qty_buy, unit_price, tt_price
            counter_n += 1
            continue
    else:
        if 'code' in info_json:
            print(info_json['code'] + ": " + info_json['message'])
            return None
        unit_price = None
        tt_price = None
        return qty_buy, unit_price, tt_price
    
# def alternate_part(info_json):
#     pass

# def get_alternate_part_price(info_json, qty_buy):
#     pass

"""TEST CASE"""
# url = get_url(info_json)
# print(url)
# qty_available = get_QOH(info_json)
# print(qty_available)
# lead_time = get_leadtime(info_json)
# print(lead_time)
# pricing = get_price(info_json, qty_buy)
# print(pricing)
# mounting_casing = get_case_mountingType(info_json)
# print(mounting_casing)