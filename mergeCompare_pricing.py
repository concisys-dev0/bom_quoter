from dk_RFQ_BOM import *
from mouser_RFQ_BOM import *
from tti_RFQ_BOM import *

import time
import sys
import re

def get_best_price(dk_ext, mouser_ext, tti_ext, dk_time, mouser_time, tti_time):
    if dk_ext < mouser_ext and dk_ext < tti_ext:
        f = "dk"
        return dk_ext, f
    elif mouser_ext < dk_ext and mouser_ext < tti_ext:
        f = "mouser"
        return mouser_ext, f
    elif tti_ext < dk_ext and tti_ext < mouser_ext:
        f = "tti"
        return tti_ext, f
    else:
        if dk_ext== sys.maxsize and mouser_ext == sys.maxsize and tti_ext == sys.maxsize:
            if dk_time<mouser_time and dk_time<mouser_time:
                f = "dk"
                return dk_ext, f
            if mouser_time<dk_time and mouser_time<tti_time:
                f = "mouser"
                return mouser_ext, f
            if tti_time<dk_time and tti_time<mouser_time:
                f = "tti"
                return tti_ext, f
        return None, None

def dk_get_info(path):
    start_time = time.time()
    dk_output = dk_get_result(path)
    # pd.read_excel(path, sheet_name = 'DK_Results')
    print("--- %s seconds ---" % (time.time() - start_time))
    return dk_output, path

def mouser_get_info(path):
    start_time = time.time()
    mouser_output = mouser_get_result(path)
    # pd.read_excel(path, sheet_name = 'Mouser_Results')
    print("--- %s seconds ---" % (time.time() - start_time))
    return mouser_output, path

def tti_get_info(path):
    start_time = time.time()
    tti_output = tti_get_result(path)
    # pd.read_excel(path, sheet_name = 'TTI_Results')
    print("--- %s seconds ---" % (time.time() - start_time))
    return tti_output, path

def get_compare_results(path):
    dk_output = dk_get_info(path)
    dk_price_list = []
    dk_notes_list = []
    dk_leadtime_list = []
    L = len(dk_output[0].axes[0])
    for i in range(L):
        dk_price = str(dk_output[0].iloc[i]['Ext'])
        dk_price_list.append(dk_price)
        dk_notes = str(dk_output[0].iloc[i]['Notes'])
        dk_notes_list.append(dk_notes)
        dk_leadtime = str(dk_output[0].iloc[i]['Lead Time'])
        dk_leadtime_list.append(dk_leadtime)
        
    dk_time = []
    for i in range(L):
        if dk_price_list[i] == 'None' or dk_price_list[i] == 'nan':
            dk_price_list[i] = sys.maxsize
        if dk_notes_list[i] == "No Stock":
            dk_price_list[i] = sys.maxsize
        elif dk_notes_list[i] == "Not Enough Stock":
            dk_price_list[i] = sys.maxsize - 3
        elif dk_notes_list[i] == "Please Check URL":
            dk_price_list[i] = sys.maxsize - 2
        if "week" in dk_leadtime_list[i]:
            n_week = int(re.findall("\d+", dk_leadtime_list[i])[0])
            # int(filter(str.isdigit, str(dk_leadtime_list[i])))
            # [int(s) for s in dk_leadtime_list[i].split() if s.isdigit()]
            n_day = n_week*7
            dk_time.append(n_day)
            dk_leadtime_list[i] = (" ".join((str(n_day), "Days")))
        else:
            dk_time.append(dk_leadtime_list[i])
        # print(dk_time[i])
        if dk_time[i] == 'None' or dk_time[i] == "nan":
            dk_time[i] = sys.maxsize
        elif dk_time[i] == "No lead time information available":
            dk_time[i] = sys.maxsize - 2

    mouser_output = mouser_get_info(path)
    mouser_price_list = []
    mouser_notes_list = []
    mouser_leadtime_list = []
    L = len(mouser_output[0].axes[0])
    for i in range(L):
        mouser_price = str(mouser_output[0].iloc[i]['Ext'])
        mouser_price_list.append(mouser_price)
        mouser_notes = str(mouser_output[0].iloc[i]['Notes'])
        mouser_notes_list.append(mouser_notes)
        mouser_leadtime = str(mouser_output[0].iloc[i]['Lead Time'])
        mouser_leadtime_list.append(mouser_leadtime)
    
    mouser_time = []
    for i in range(L):
        if mouser_price_list[i] == 'None' or mouser_price_list[i] == 'nan':
            mouser_price_list[i] = sys.maxsize
        if mouser_notes_list[i] == "No Stock":
            mouser_price_list[i] = sys.maxsize
        elif mouser_notes_list[i] == "Not Enough Stock":
            mouser_price_list[i] = sys.maxsize - 3
        elif mouser_notes_list[i] == "Please Check URL":
            mouser_price_list[i] = sys.maxsize - 2
        if "Days" in mouser_leadtime_list[i]:
            n_day = int(re.findall("\d+", mouser_leadtime_list[i])[0])
            mouser_time.append(n_day)
        else:
            mouser_time.append(mouser_leadtime_list[i])
        # print(mouser_time[i])
        if mouser_time[i] == 'None' or mouser_time[i] == "nan":
            mouser_time[i] = sys.maxsize
        elif mouser_time[i] == 0:
            mouser_time[i] = sys.maxsize
    
    tti_output = tti_get_info(path)
    tti_price_list = []
    tti_notes_list = []
    tti_leadtime_list = []
    L = len(tti_output[0].axes[0])
    for i in range(L):
        tti_price = str(tti_output[0].iloc[i]['Ext'])
        tti_price_list.append(tti_price)
        tti_notes = str(tti_output[0].iloc[i]['Notes'])
        tti_notes_list.append(tti_notes)
        tti_leadtime = str(tti_output[0].iloc[i]['Lead Time'])
        tti_leadtime_list.append(tti_leadtime)
    # print(tti_notes_list)
    tti_time = []
    for i in range(L):
        if tti_price_list[i] == 'None' or tti_price_list[i] == 'nan':
            tti_price_list[i] = sys.maxsize
        if tti_notes_list[i] == "No Stock":
            tti_price_list[i] = sys.maxsize
        elif tti_notes_list[i] == "Not Enough Stock":
            tti_price_list[i] = sys.maxsize - 3
        elif tti_notes_list[i] == "Please Check URL":
            tti_price_list[i] = sys.maxsize - 2
        if "Week" in tti_leadtime_list[i]:
            n_week = int(re.findall("\d+", tti_leadtime_list[i])[0])
            # int(filter(str.isdigit, str(tti_leadtime_list[i])))
            # [int(s) for s in tti_leadtime_list[i].split() if s.isdigit()]
            n_day = n_week*7
            tti_time.append(n_day)
            tti_leadtime_list[i] = (" ".join((str(n_day), "Days")))
        else:
            tti_time.append(tti_leadtime_list[i])
        # print(tti_time[i])
        if tti_time[i] == 'None' or tti_time[i] == "nan":
            tti_time[i] = sys.maxsize
        elif tti_time[i] == "Contact TTI":
            tti_time[i] = sys.maxsize - 2

    best_prices = []
    sheet_name = []
    for i in range(L):
        best_price = get_best_price(float(dk_price_list[i]), float(mouser_price_list[i]), float(tti_price_list[i]), dk_time[i], mouser_time[i], tti_time[i])
        best_prices.append(best_price[0])
        sheet_name.append(best_price[1])

    output_row = sheet_name
    for r in range(len(sheet_name)):
        if sheet_name[r] == "dk":
            output_row[r] = dk_output[0].iloc[r]
        elif sheet_name[r] == "mouser":
            output_row[r] = mouser_output[0].iloc[r]
        elif sheet_name[r] == "tti":
            output_row[r] = tti_output[0].iloc[r]
        else:
            output_row[r] = dk_output[0].iloc[r]
    
    dk_mounting_list = []
    dk_casing_list = []
    dk_n_termination_list = []
    L = len(dk_output[0].axes[0])
    for i in range(L):
        dk_mount = str(dk_output[0].iloc[i]['Mounting Type'])
        if dk_mount == "None":
            dk_mounting_list.append(None)
        else:
            dk_mounting_list.append(dk_mount)
        dk_case = str(dk_output[0].iloc[i]['Package/Case'])
        if dk_case == "None":
            dk_casing_list.append(None)
        else:
            dk_casing_list.append(dk_case)
        dk_termination = dk_output[0].iloc[i]['Number of Termination']
        if dk_termination == "None":
            dk_n_termination_list.append(None)
        else:
            dk_n_termination_list.append(dk_termination)
        
    output_df = pd.DataFrame(output_row, columns=['Item','Internal  P/ N','Description','Reference Designators','Manufacturer Part Number', 'Manufacturer', 'Quantity', 'Qty Need', 'Qty Buy', 
                                      'Unit Price', 'Ext', 'Excess', 'Lead Time', 'Q O H', 'Notes', 'Supplier', 'URL', 'Mounting Type', 'Package/Case', 'TTI Min Buy Qty', 'Number of Termination'])
    output_df['Mounting Type'] = dk_mounting_list
    output_df['Package/Case'] = dk_casing_list
    output_df['Number of Termination'] = dk_n_termination_list
    with pd.ExcelWriter(path, mode = "a", engine = 'openpyxl', if_sheet_exists = "replace") as writer:
        output_df.to_excel(writer, sheet_name='Best_Prices', index=False)
    return output_df
# if_sheet_exists = "new"
"""TEST CASE"""
# path = r"C:\Users\Lan\Documents\API requests\test doc\BOM-PCA_Optics_Test_Tool_Main_216673(DEV)-RFQtester.xlsx"
# start_time = time.time()
# results = get_compare_results(path)
# print("--- %s seconds ---" % (time.time() - start_time))
