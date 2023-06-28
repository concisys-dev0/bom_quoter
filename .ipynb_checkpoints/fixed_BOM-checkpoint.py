from fc_bs4_scraping import*
from mergeCompare_pricing import*
import pandas as pd
import numpy as np
import openpyxl
import time
import sys

def getInfo(output_df):
    best_price_df = output_df
    part_list = []
    manufacture_list = []
    mountType_list = []
    case_list = []
    desc_list = []
    ulr_list = []
    supplier_list = []
    n_termination = []
    L = len(best_price_df.axes[0])

    for i in range(L):
        part_id = str(best_price_df.iloc[i]['Manufacturer Part Number'])
        part_list.append(part_id)
        manufacture = str(best_price_df.iloc[i]['Manufacturer'])
        manufacture_list.append(manufacture)
        mountType = str(best_price_df.iloc[i]['Mounting Type'])
        mountType_list.append(mountType)
        casing = str(best_price_df.iloc[i]['Package/Case'])
        case_list.append(casing)
        desc = str(best_price_df.iloc[i]['Description'])
        desc_list.append(desc)
        urls = str(best_price_df.iloc[i]['URL'])
        ulr_list.append(urls)
        supplier = str(best_price_df.iloc[i]['Supplier'])
        supplier_list.append(supplier)
        n_pin = str(best_price_df.iloc[i]['Number of Termination'])
        n_termination.append(n_pin)
        
    print(mountType_list)
    print(case_list)
    print(n_termination)

    for i in range(L):
        if ("Surface Mount" in mountType_list[i]):
            mountType_list[i] = "SMT"
        if ("SURFACE MOUNT" in mountType_list[i]):
            mountType_list[i] = "SMT"
        if "Through Hole" in mountType_list[i]:
            mountType_list[i] = "TH"
        if "THROUGH HOLE" in mountType_list[i]:
            mountType_list[i] = "TH"
        if "Mechanic" in mountType_list[i]:
            mountType_list[i] = "MEC"
        if (mountType_list[i] != 'None' and case_list[i] != 'None') or (mountType_list[i] != 'nan' and case_list[i] != 'nan'): # or (mountType_list[i] != None and case_list[i] != None)
            if ("008004" in case_list[i]) or ("0201" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("0075" in case_list[i]) or ("0301" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("01005" in case_list[i]) or ("0402" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("15015" in case_list[i]) or ("0404" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("0201" in case_list[i]) or ("0603" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("0202" in case_list[i]) or ("0505" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("0302" in case_list[i]) or ("0805" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("0303" in case_list[i]) or ("0808" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("0504" in case_list[i]) or ("1310" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("0402" in case_list[i]) or ("1005" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("0603" in case_list[i]) or ("1608" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("0805" in case_list[i]) or ("2012" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("1008" in case_list[i]) or ("2520" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("1111" in case_list[i]) or ("2828" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("1206" in case_list[i]) or ("3216" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("1210" in case_list[i]) or ("3225" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("1410" in case_list[i]) or ("3625" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("1515" in case_list[i]) or ("3838" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("1806" in case_list[i]) or ("4516" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("1808" in case_list[i]) or ("4520" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("1812" in case_list[i]) or ("4532" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("1825" in case_list[i]) or ("4564" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("2010" in case_list[i]) or ("5025" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("2020" in case_list[i]) or ("5050" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("2220" in case_list[i]) or ("5750" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("2225" in case_list[i]) or ("5764" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("2512" in case_list[i]) or ("6432" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("2520" in case_list[i]) or ("6450" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("2917" in case_list[i]) or ("7343" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("2920" in case_list[i]) or ("7450" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("3333" in case_list[i]) or ("8484" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("3640" in case_list[i]) or ("9210" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("4040" in case_list[i]) or ("100100" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("5550" in case_list[i]) or ("140127" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            if ("8060" in case_list[i]) or ("203153" in case_list[i]):
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
                mountType_list[i] = "SMT"
            else:
                if  ('nan' in case_list[i]) or'None' in case_list[i]: # 'nan'
                    case_list[i] = None
                if ('nan' in mountType_list[i]) or 'None' in mountType_list[i]: # 'nan'
                    mountType_list[i] = None
        if (mountType_list[i] == 'None' and case_list[i] != 'None') or (mountType_list[i] == 'nan' and case_list[i] != 'nan'): # or (mountType_list[i] == None and case_list[i] != None)
            if "BGA" in case_list[i]:
                mountType_list[i] = "SMT"
            if "CGA" in case_list[i]:
                mountType_list[i] = "SMT"
            if "DIM" in case_list[i]:
                mountType_list[i] = "SMT"
            if "DIP" in case_list[i]:
                mountType_list[i] = "SMT"
            if "DSO" in case_list[i]:
                mountType_list[i] = "SMT"
            if "DSB" in case_list[i]:
                mountType_list[i] = "SMT"
            if "LGA" in case_list[i]:
                mountType_list[i] = "SMT"
            if "PGA" in case_list[i]:
                mountType_list[i] = "SMT"
            if "QFF" in case_list[i]:
                mountType_list[i] = "SMT"
            if "QFJ" in case_list[i]:
                mountType_list[i] = "SMT"
            if "QFN" in case_list[i]:
                mountType_list[i] = "SMT"
            if "QFP" in case_list[i]:
                mountType_list[i] = "SMT"
            if "SIM" in case_list[i]:
                mountType_list[i] = "SMT"
            if "SIP" in case_list[i]:
                mountType_list[i] = "SMT"
            if "SKT" in case_list[i]:
                mountType_list[i] = "SMT"
            if "SOF" in case_list[i]:
                mountType_list[i] = "SMT"
            if "SOJ" in case_list[i]:
                mountType_list[i] = "SMT"
            if "SON" in case_list[i]:
                mountType_list[i] = "SMT"
            if "SVP" in case_list[i]:
                mountType_list[i] = "SMT"
            if "UCI" in case_list[i]:
                mountType_list[i] = "SMT"
            if "WLB" in case_list[i]:
                mountType_list[i] = "SMT"
            if "ZIP" in case_list[i]:
                mountType_list[i] = "SMT"
            if "SMD" in case_list[i]:
                mountType_list[i] = "SMT"
            if "SMT" in case_list[i]:
                mountType_list[i] = "SMT"
            if "Surface Mount" in case_list[i]:
                mountType_list[i] = "SMT"
            if ("008004" in case_list[i]) or ("0201" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0075" in case_list[i]) or ("0301" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("01005" in case_list[i]) or ("0402" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("15015" in case_list[i]) or ("0404" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0201" in case_list[i]) or ("0603" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0202" in case_list[i]) or ("0505" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0302" in case_list[i]) or ("0805" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0303" in case_list[i]) or ("0808" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0504" in case_list[i]) or ("1310" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0402" in case_list[i]) or ("1005" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0603" in case_list[i]) or ("1608" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0805" in case_list[i]) or ("2012" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1008" in case_list[i]) or ("2520" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1111" in case_list[i]) or ("2828" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1206" in case_list[i]) or ("3216" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1210" in case_list[i]) or ("3225" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1410" in case_list[i]) or ("3625" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1515" in case_list[i]) or ("3838" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1806" in case_list[i]) or ("4516" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1808" in case_list[i]) or ("4520" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1812" in case_list[i]) or ("4532" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1825" in case_list[i]) or ("4564" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("2010" in case_list[i]) or ("5025" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("2020" in case_list[i]) or ("5050" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("2220" in case_list[i]) or ("5750" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("2225" in case_list[i]) or ("5764" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("2512" in case_list[i]) or ("6432" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("2520" in case_list[i]) or ("6450" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("2917" in case_list[i]) or ("7343" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("2920" in case_list[i]) or ("7450" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("3333" in case_list[i]) or ("8484" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("3640" in case_list[i]) or ("9210" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("4040" in case_list[i]) or ("100100" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("5550" in case_list[i]) or ("140127" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("8060" in case_list[i]) or ("203153" in case_list[i]):
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            else:
                if ('nan' in case_list[i]) or 'None' in case_list[i]: # 'nan'
                    case_list[i] = None
                if ('nan' in mountType_list[i]) or 'None' in mountType_list[i]: # 'nan'
                    mountType_list[i] = None
        if (mountType_list[i] == 'None' and case_list[i] == 'None') or (mountType_list[i] == 'nan' and case_list[i] == 'nan'): # or (mountType_list[i] == None and case_list[i] == None)
            if ("008004" in desc_list[i]) or ("0201" in desc_list[i]):
                case_list[i] = "008004"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0075" in desc_list[i]) or ("0301" in desc_list[i]):
                case_list[i] = "0075"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("01005" in desc_list[i]) or ("0402" in desc_list[i]):
                case_list[i] = "01005"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("15015" in desc_list[i]) or ("0404" in desc_list[i]):
                case_list[i] = "15015"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0201" in desc_list[i]) or ("0603" in desc_list[i]):
                case_list[i] = "0201"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0202" in desc_list[i]) or ("0505" in desc_list[i]):
                case_list[i] = "0202"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0302" in desc_list[i]) or ("0805" in desc_list[i]):
                case_list[i] = "0302"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0303" in desc_list[i]) or ("0808" in desc_list[i]):
                case_list[i] = "0303"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0504" in desc_list[i]) or ("1310" in desc_list[i]):
                case_list[i] = "0504"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0402" in desc_list[i]) or ("1005" in desc_list[i]):
                case_list[i] = "0402"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0603" in desc_list[i]) or ("1608" in desc_list[i]):
                case_list[i] = "0603"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("0805" in desc_list[i]) or ("2012" in desc_list[i]):
                case_list[i] = "0805"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1008" in desc_list[i]) or ("2520" in desc_list[i]):
                case_list[i] = "1008"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1111" in desc_list[i]) or ("2828" in desc_list[i]):
                case_list[i] = "1111"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1206" in desc_list[i]) or ("3216" in desc_list[i]):
                case_list[i] = "1206"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1210" in desc_list[i]) or ("3225" in desc_list[i]):
                case_list[i] = "1210"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1410" in desc_list[i]) or ("3625" in desc_list[i]):
                case_list[i] = "1410"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1515" in desc_list[i]) or ("3838" in desc_list[i]):
                case_list[i] = "1515"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1806" in desc_list[i]) or ("4516" in desc_list[i]):
                case_list[i] = "1806"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1808" in desc_list[i]) or ("4520" in desc_list[i]):
                case_list[i] = "1808"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1812" in desc_list[i]) or ("4532" in desc_list[i]):
                case_list[i] = "1812"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("1825" in desc_list[i]) or ("4564" in desc_list[i]):
                case_list[i] = "1825"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("2010" in desc_list[i]) or ("5025" in desc_list[i]):
                case_list[i] = "2010"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("2020" in desc_list[i]) or ("5050" in desc_list[i]):
                case_list[i] = "2020"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("2220" in desc_list[i]) or ("5750" in desc_list[i]):
                case_list[i] = "2220"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("2225" in desc_list[i]) or ("5764" in desc_list[i]):
                case_list[i] = "2225"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("2512" in desc_list[i]) or ("6432" in desc_list[i]):
                case_list[i] = "2512"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("2520" in desc_list[i]) or ("6450" in desc_list[i]):
                case_list[i] = "2520"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("2917" in desc_list[i]) or ("7343" in desc_list[i]):
                case_list[i] = "2917"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("2920" in desc_list[i]) or ("7450" in desc_list[i]):
                case_list[i] = "2920"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("3333" in desc_list[i]) or ("8484" in desc_list[i]):
                case_list[i] = "3333"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("3640" in desc_list[i]) or ("9210" in desc_list[i]):
                case_list[i] = "3640"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("4040" in desc_list[i]) or ("100100" in desc_list[i]):
                case_list[i] = "4040"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("5550" in desc_list[i]) or ("140127" in desc_list[i]):
                case_list[i] = "5550"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if ("8060" in desc_list[i]) or ("203153" in desc_list[i]):
                case_list[i] = "8060"
                mountType_list[i] = "SMT"
                if n_termination[i] == None or n_termination[i] == 'None' or n_termination[i] == 'nan':
                    n_termination[i] = 2
            if "SMD" in desc_list[i]:
                mountType_list[i] = "SMT"
            if "SMT" in desc_list[i]:
                mountType_list[i] = "SMT"
            if "Surface Mount" in desc_list[i]:
                mountType_list[i] = "SMT"
            else:
                if 'nan' in mountType_list[i] or ('None' in mountType_list[i]): # 
                    mountType_list[i] = None
        # if 'nan' in case_list[i]: # 'nan' in case_list[i] or
        #     [i] = None
        # if'nan' in supplier_list[i]: # 'nan' in supplier_list[i] or 
        #     ulr_list[i] = None

    best_price_df['Mounting Type'] = mountType_list
    best_price_df['Package/Case'] = case_list
    best_price_df['Number of Termination'] = n_termination
    return best_price_df

def getInfo_2(output_df):
    best_price_df = output_df
    part_list = []
    manufacture_list = []
    mountType_list = []
    case_list = []
    # desc_list = []
    n_termination = []
    L = len(best_price_df.axes[0])

    for i in range(L):
        part_id = str(best_price_df.iloc[i]['Manufacturer Part Number'])
        part_list.append(part_id)
        manufacture = str(best_price_df.iloc[i]['Manufacturer'])
        manufacture_list.append(manufacture)
        mountType = str(best_price_df.iloc[i]['Mounting Type'])
        mountType_list.append(mountType)
        casing = str(best_price_df.iloc[i]['Package/Case'])
        case_list.append(casing)
        # desc = str(best_price_df.iloc[i]['Description'])
        # desc_list.append(desc)
        termination = str(best_price_df.iloc[i]['Number of Termination'])
        n_termination.append(termination)
        
    for i in range(L):
        if n_termination[i] == "nan" or n_termination[i] == "None":
            if "-SMD" in case_list[i]:
                term_n = int(re.findall("\d+", case_list[i])[-1])
                n_termination[i] = term_n
            if "PIN" in case_list[i]:
                term_n = int(re.findall("\d+", case_list[i])[-1])
                n_termination[i] = term_n
            else:
                n_termination[i] = None
                if case_list[i] != None:
                    term_n = re.match("\d.*.*-", case_list[i])
                    if term_n != None:
                        print(term_n.group(0))
                        term_n = int(re.findall("\d+",case_list[i])[0])
                        n_termination[i] = term_n
                    else:
                        if "," in  case_list[i]:
                            result = [x.strip() for x in  case_list[i].split(',')]
                            # print(result)
                            for n in range(len(result)):
                                term_n = re.match(".*-\d.*.*-\d.*", result[n])
                                if term_n != None:
                                    print(term_n.group(0))
                                    if len(term_n.group(0)) > 1:
                                        term_n = int(re.findall("\d+", result[n])[1])
                                        n_termination[i] = term_n
                        else:
                            term_n = re.match(".*-\d.*.*-\d.*", case_list[i])
                            if term_n != None:
                                print(term_n.group(0))
                                if len(term_n.group(0)) > 1:
                                    term_n = int(re.findall("\d+", case_list[i])[1])
                                    n_termination[i] = term_n
    
    print(n_termination)
    best_price_df['Number of Termination'] = n_termination
    return best_price_df
    
def scrape_saved(path):
    output_df = get_compare_results(path)
    df = getInfo(output_df)
    part_list = []
    manufacture_list = []
    mountType_list = []
    case_list = []
    ulr_list = []
    L = len(df.axes[0])
    print(L)

    for i in range(L):
        part_id = str(df.iloc[i]['Manufacturer Part Number'])
        part_list.append(part_id)
        manufacture = str(df.iloc[i]['Manufacturer'])
        manufacture_list.append(manufacture)
        mountType = str(df.iloc[i]['Mounting Type'])
        mountType_list.append(mountType)
        casing = str(df.iloc[i]['Package/Case'])
        case_list.append(casing)
        urls = str(df.iloc[i]['URL'])
        ulr_list.append(urls)
    
    l = len(ulr_list)
    for i in range(l):
        if part_list[i] == 'nan' and manufacture_list[i]== 'nan':
            part_list[i] = None
            manufacture_list[i] = None
            mountType_list[i] = None
            case_list[i] = None
            ulr_list[i] = None
            continue
        if (case_list[i] == 'None' and mountType_list[i] == 'None') or (case_list[i] == 'nan' and mountType_list[i] == 'nan'):
            pairs = fc_get_part_info(str(part_list[i]), manufacture_list[i])
            mountType_list[i] = pairs[0]
            case_list[i] = pairs[1]
            ulr_list[i] = pairs[2]
        elif case_list[i] == 'None' or case_list[i] == 'nan':
            pairs = fc_get_part_info(str(part_list[i]), manufacture_list[i])
            case_list[i] = pairs[1]
            ulr_list[i] = pairs[2]
        elif mountType_list[i] == 'None' or mountType_list[i] == 'nan':
            pairs = fc_get_part_info(str(part_list[i]), manufacture_list[i])
            mountType_list[i] = pairs[0]
            ulr_list[i] = pairs[2]
        elif ulr_list[i] == 'None' or ulr_list[i] == 'nan':
            pairs = fc_get_part_info(str(part_list[i]), manufacture_list[i])
            ulr_list[i] = pairs[2]

    df['Mounting Type'] = mountType_list
    df['Package/Case'] = case_list
    df['URL'] = ulr_list
    df_r = getInfo(df)
    df_r2 = getInfo_2(df_r)
    with pd.ExcelWriter(path, mode = "a", engine = 'openpyxl', if_sheet_exists = "replace") as writer:
        df_r2.to_excel(writer, sheet_name='Best_Prices', index=False)
    return df_r2
"""TEST CASE"""
# path = r"C:\Users\Lan\Documents\API requests\test doc\RFQ BUY BOM 42102 Rev A_qty 10_2023Mar07_083939AM-0800binT-RFQtester.xlsx"
path = "D:\ExcessParts\BOM\BOM TEST.xlsx"

start_time = time.time()
df_r = scrape_saved(path)
print("--- %s seconds ---" % (time.time() - start_time))