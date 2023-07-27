from dk_RFQ_BOM import *
from mouser_RFQ_BOM import *
from tti_RFQ_BOM import *

import time
import sys
import re

"""Taking result from Digikey, Mouser, TTI API and compare price for the lowest one"""
# Compare product price and if it need request too order take one with shortest lead time
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

# Return Digikey API result
def dk_get_info(path):
    start_time = time.time()
    try:
        dk_output = pd.read_excel(path, sheet_name = 'DK_Results') # Use when don't need API, already have sheet DK_Results in Excel
    except ValueError:
        dk_output = dk_get_result(path)
    print("Digikey Done: 1/3 completed")
    # print("--- %s seconds ---" % (time.time() - start_time))
    return dk_output, path

# Return TTI API result
def tti_get_info(path):
    start_time = time.time()
    try:
        tti_output = pd.read_excel(path, sheet_name = 'TTI_Results') # Use when don't need API, already have sheet TTI_Results in Excel
    except ValueError:
        tti_output = tti_get_result(path)
    print("TTI Done: 2/3 completed")
    # print("--- %s seconds ---" % (time.time() - start_time))
    return tti_output, path

# Return Mouser API result
def mouser_get_info(path):
    start_time = time.time()
    try:
        mouser_output = pd.read_excel(path, sheet_name = 'Mouser_Results') # Use when don't need API or already have sheet Mouser_Results in Excel
    except ValueError:
        mouser_output = mouser_get_result(path)
    print("Mouser Done: 3/3 completed")
    # print("--- %s seconds ---" % (time.time() - start_time))
    return mouser_output, path

# Choose Qty order price to compare
def compare_options_result(path):
    # Default to compare Qty Buy if input does not match Qty Order
    time.sleep(1)
    print("\nEnter the qty order 'Buy' value you would like to compare.")
    print("For example, if you would like to compare Q1 qty orders, then enter 'Q1 Buy'; if comparing Q2 qty orders, then enter 'Q2 Buy'; and so on and so forth.")
    print("\nIf you do not have a Qty Order to compare, then please enter 'Qty Buy' for the best results.")
    print("-----------------------------------------------------------------------")
    qty_order = input("Please enter your choosen column(s): ")
    print("\nQuoting the BOM. Please wait.") # tells user that bom quoting process is starting
    if qty_order == "Qty Buy":
        compare_column = "Ext"
        result = get_compare_results(path, compare_column)
    elif qty_order == "Q1 Buy":
        compare_column = "Q1 Ext"
        try:
            result = get_compare_results(path, compare_column)
        except KeyError:
            result = get_compare_results(path, compare_column = "Ext")
    elif qty_order == "Q2 Buy":
        compare_column = "Q2 Ext"
        try:
            result = get_compare_results(path, compare_column)
        except KeyError:
            result = get_compare_results(path, compare_column = "Ext")
    elif qty_order == "Q3 Buy":
        compare_column = "Q3 Ext"
        try:
            result = get_compare_results(path, compare_column)
        except KeyError:
            result = get_compare_results(path, compare_column = "Ext")
    elif qty_order == "Q4 Buy":
        compare_column = "Q4 Ext"
        try:
            result = get_compare_results(path, compare_column)
        except KeyError:
            result = get_compare_results(path, compare_column = "Ext")
    elif qty_order == "Q5 Buy":
        compare_column = "Q5 Ext"
        try:
            result = get_compare_results(path, compare_column)
        except KeyError:
            result = get_compare_results(path, compare_column = "Ext")
    else:
        result = get_compare_results(path, compare_column = "Ext")
    return result

# Return results of comparation and combine them into new sheet
def get_compare_results(path, compare_column):
    # Setup Digikey info to compare pricing and lead time
    dk_output = dk_get_info(path)
    # print(dk_output)
    dk_price_list = []
    dk_notes_list = []
    dk_leadtime_list = []
    L = len(dk_output[0].axes[0])
    for i in range(L):
        dk_price = str(dk_output[0].iloc[i][compare_column]) # 'Ext'
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
            dk_price_list[i] = sys.maxsize - 30
        elif dk_notes_list[i] == "Please Check URL":
            dk_price_list[i] = sys.maxsize - 20
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
            dk_time[i] = sys.maxsize - 20
    # Setup TTI info to compare pricing and lead time
    tti_output = tti_get_info(path)
    tti_price_list = []
    tti_notes_list = []
    tti_leadtime_list = []
    L = len(tti_output[0].axes[0])
    for i in range(L):
        tti_price = str(tti_output[0].iloc[i][compare_column]) # 'Ext'
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
            tti_price_list[i] = sys.maxsize - 30
        elif tti_notes_list[i] == "Please Check URL":
            tti_price_list[i] = sys.maxsize - 20
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
            tti_time[i] = sys.maxsize - 20
    # Setup Mouser info to compare pricing and lead time
    mouser_output = mouser_get_info(path)
    mouser_price_list = []
    mouser_notes_list = []
    mouser_leadtime_list = []
    L = len(mouser_output[0].axes[0])
    for i in range(L):
        mouser_price = str(mouser_output[0].iloc[i][compare_column]) # 'Ext'
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
            mouser_price_list[i] = sys.maxsize - 30
        elif mouser_notes_list[i] == "Please Check URL":
            mouser_price_list[i] = sys.maxsize - 20
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

    best_prices = []
    sheet_name = []
    for i in range(L): # Pass info to compare function
        best_price = get_best_price(float(dk_price_list[i]), float(mouser_price_list[i]), float(tti_price_list[i]), dk_time[i], mouser_time[i], tti_time[i])
        best_prices.append(best_price[0])
        sheet_name.append(best_price[1])

    output_row = sheet_name
    for r in range(len(sheet_name)): # Copy the lowest price product row from  result sheet to new df
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
    for i in range(L): # Default info about mounting type, package/case, and terminals from Digikey to df
        dk_mount = str(dk_output[0].iloc[i]['Mounting Type'])
        if dk_mount == "None" or dk_mount == "nan":
            dk_mounting_list.append(None)
        else:
            dk_mounting_list.append(dk_mount)
        dk_case = str(dk_output[0].iloc[i]['Package/Case'])
        if dk_case == "None" or dk_case == "nan":
            dk_casing_list.append(None)
        else:
            dk_casing_list.append(dk_case)
        dk_termination = dk_output[0].iloc[i]['Terminations']
        if dk_termination == "None" or dk_termination == "nan":
            dk_n_termination_list.append(None)
        else:
            dk_n_termination_list.append(dk_termination)
    # Set column names
    output_df = pd.DataFrame(output_row, columns=['Item','Internal P/N','Description','Reference Designators','Comment','Manufacturer Part Number', 'Manufacturer', 'Quantity', 'Qty Need', 'Qty Buy','Unit Price', 'Ext', 'Excess', 'Lead Time', 'Q O H', 'Notes', 'Supplier', 'Mounting Type', 'Package/Case', 'Terminations', 'TTI Min Buy Qty', 
                                                  'Q1 Need', 'Q1 Buy', 'Min Q1 Buy', 'Q1 Unit Price', 'Q1 Ext', 'Q1 Excess', 
                                                  'Q2 Need', 'Q2 Buy', 'Min Q2 Buy', 'Q2 Unit Price', 'Q2 Ext', 'Q2 Excess', 
                                                  'Q3 Need', 'Q3 Buy', 'Min Q3 Buy', 'Q3 Unit Price', 'Q3 Ext', 'Q3 Excess', 
                                                  'Q4 Need', 'Q4 Buy', 'Min Q4 Buy', 'Q4 Unit Price', 'Q4 Ext', 'Q4 Excess', 
                                                  'Q5 Need', 'Q5 Buy', 'Min Q5 Buy', 'Q5 Unit Price', 'Q5 Ext', 'Q5 Excess', 'URL'])
    output_df['Mounting Type'] = dk_mounting_list
    output_df['Package/Case'] = dk_casing_list
    output_df['Terminations'] = dk_n_termination_list
    return output_df

"""TEST CASE"""
# if __name__ in "__main__":
#     path = r"C:\Users\Lan\Documents\bom_quoter\BOM-sample\05-072889-01-a-test.xlsx"
#     start_time = time.time()
#     results = compare_options_result(path)
#     print("--- %s seconds ---" % (time.time() - start_time))