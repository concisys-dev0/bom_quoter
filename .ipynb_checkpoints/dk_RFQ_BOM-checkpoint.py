from dk_keyword_buy_info import*
from input_BOM import*
from df_styling import*
from dk_oauth2_token import get_change_user
import time

"""Return info gather from Digikey API to dataframe and save results to Excel original file as sheet name is DK_Results"""
def dk_get_result(path):
    input_list = setup_BOM_info(path) # Function from input_BOM.py
    # input_list is tuple contains df, part_list, manufacture_list, qty_buy_list, qty_need_list
    df = input_list[0]
    part_list = input_list[1]
    manufacture_list = input_list[2]
    qty_buy_list = input_list[3]
    qty_need_list = input_list[4]
    i = 0
    L = len(part_list) #length of df (also number of part to be search)
    # If the sheet1 qty order 1, 2, 3, 4, 5 is filled
    if len(input_list) == 7: # Break 1
        qty_b1_list = input_list[5]
        qty_b1_buy_list = input_list[6]
        qty_b1_unit_price = []
        qty_b1_ext = []
        qty_b1_excess = []
    elif len(input_list) == 9: # Break 2
        qty_b1_list = input_list[5]
        qty_b1_buy_list = input_list[6]
        qty_b1_unit_price = []
        qty_b1_ext = []
        qty_b1_excess = []
        qty_b2_list = input_list[7]
        qty_b2_buy_list = input_list[8]
        qty_b2_unit_price = []
        qty_b2_ext = []
        qty_b2_excess = []
    elif len(input_list) == 11: # Break 3
        qty_b1_list = input_list[5]
        qty_b1_buy_list = input_list[6]
        qty_b1_unit_price = []
        qty_b1_ext = []
        qty_b1_excess = []
        qty_b2_list = input_list[7]
        qty_b2_buy_list = input_list[8]
        qty_b2_unit_price = []
        qty_b2_ext = []
        qty_b2_excess = []
        qty_b3_list = input_list[9]
        qty_b3_buy_list = input_list[10]
        qty_b3_unit_price = []
        qty_b3_ext = []
        qty_b3_excess = []
    elif len(input_list) == 13: # Break 4
        qty_b1_list = input_list[5]
        qty_b1_buy_list = input_list[6]
        qty_b1_unit_price = []
        qty_b1_ext = []
        qty_b1_excess = []
        qty_b2_list = input_list[7]
        qty_b2_buy_list = input_list[8]
        qty_b2_unit_price = []
        qty_b2_ext = []
        qty_b2_excess = []
        qty_b3_list = input_list[9]
        qty_b3_buy_list = input_list[10]
        qty_b3_unit_price = []
        qty_b3_ext = []
        qty_b3_excess = []
        qty_b4_list = input_list[11]
        qty_b4_buy_list = input_list[12]
        qty_b4_unit_price = []
        qty_b4_ext = []
        qty_b4_excess = []
    elif len(input_list) == 15: # Break 5
        qty_b1_list = input_list[5]
        qty_b1_buy_list = input_list[6]
        qty_b1_unit_price = []
        qty_b1_ext = []
        qty_b1_excess = []
        qty_b2_list = input_list[7]
        qty_b2_buy_list = input_list[8]
        qty_b2_unit_price = []
        qty_b2_ext = []
        qty_b2_excess = []
        qty_b3_list = input_list[9]
        qty_b3_buy_list = input_list[10]
        qty_b3_unit_price = []
        qty_b3_ext = []
        qty_b3_excess = []
        qty_b4_list = input_list[11]
        qty_b4_buy_list = input_list[12]
        qty_b4_unit_price = []
        qty_b4_ext = []
        qty_b4_excess = []
        qty_b5_list = input_list[13]
        qty_b5_buy_list = input_list[14]
        qty_b5_unit_price = []
        qty_b5_ext = []
        qty_b5_excess = []
    # List initial
    unit_price = []
    ext = []
    excess = []
    leadtime = []
    Notes = [] # [None]*L
    qty_available = []
    Supplier =[]
    a_qty_buy = []
    mountingType = []
    packageSize = []
    link = []
    n_termination_list = []
    for i in range(L):
        if i % 119 == 0 and i != 0: # rate limit only allow 120 request per minute
            time.sleep(60)
        """iterate through input list"""
        # Make sure all the list is in the same length L
        # Any .append(None) keep blank cell in Excel and satisfied require length equal L
        if part_list[i] == "nan" or part_list[i] == "None": # Manufacturer part number cell is blank
            unit_price.append(None)
            ext.append(None)
            excess.append(None)
            leadtime.append(None)
            Notes.append(None)
            qty_available.append(None)
            Supplier.append(None)
            a_qty_buy.append(None)
            mountingType.append(None)
            packageSize.append(None)
            link.append(None)
            n_termination_list.append(None)
            try:
                qty_b1_unit_price.append(None)
                qty_b1_ext.append(None)
                qty_b1_excess.append(None)
            except NameError:
                pass
            try:
                qty_b2_unit_price.append(None)
                qty_b2_ext.append(None)
                qty_b2_excess.append(None)
            except NameError:
                pass
            try:
                qty_b3_unit_price.append(None)
                qty_b3_ext.append(None)
                qty_b3_excess.append(None)
            except NameError:
                pass
            try:
                qty_b4_unit_price.append(None)
                qty_b4_ext.append(None)
                qty_b4_excess.append(None)
            except NameError:
                pass
            try:
                qty_b5_unit_price.append(None)
                qty_b5_ext.append(None)
                qty_b5_excess.append(None)
            except NameError:
                pass
            continue
        if qty_buy_list[i] == 0 or qty_buy_list[i] == "None": # Don't need to buy
            unit_price.append(None)
            ext.append(None)
            excess.append(None)
            leadtime.append(None)
            Notes.append(None)
            qty_available.append(None)
            Supplier.append(None)
            a_qty_buy.append(None)
            mountingType.append(None)
            packageSize.append(None)
            link.append(None)
            n_termination_list.append(None)
            try:
                qty_b1_unit_price.append(None)
                qty_b1_ext.append(None)
                qty_b1_excess.append(None)
            except NameError:
                pass
            try:
                qty_b2_unit_price.append(None)
                qty_b2_ext.append(None)
                qty_b2_excess.append(None)
            except NameError:
                pass
            try:
                qty_b3_unit_price.append(None)
                qty_b3_ext.append(None)
                qty_b3_excess.append(None)
            except NameError:
                pass
            try:
                qty_b4_unit_price.append(None)
                qty_b4_ext.append(None)
                qty_b4_excess.append(None)
            except NameError:
                pass
            try:
                qty_b5_unit_price.append(None)
                qty_b5_ext.append(None)
                qty_b5_excess.append(None)
            except NameError:
                pass
            continue
        # print(part_lsist[i])
        info_json = get_digikey_keyword_search(part_list[i]) # Function from dk_search_info.py
        if 'ErrorMessage' in info_json: # Error occurs
            err_m = str(info_json['ErrorMessage'])
            # print(info_json['ErrorMessage'])
            print("\nDigikey Token Error: ", info_json['ErrorDetails'])
            if err_m in ["Daily Ratelimit exceeded", "The Bearer token is invalid"] :
                print("\nRetrying with new credentials. Please refrain from interacting with the program while retry is in progress...")
                # token = get_change_user(err_m) # L Version: Function from dk_oauth2_token.py; ensure change user and get new access token
                token = get_change_user() # M Version: dk_oauth2_token.get_change_user() -> get new credentials and access token
                print("New access token: " + token)
                info_json = get_digikey_keyword_search(part_list[i])
            elif err_m == "Bearer token  expired":
                print("\nRefreshing token. Please wait.")
                refresh_token_digikey_api() # Function from dk_oauth2_token.py; get new access token from refresh token
                info_json = get_digikey_keyword_search(part_list[i]) # Retry to get info
            else:
                raise AttributeError("Digikey API authentication errored out:", str(err_m))
        # Take return of get_digikey_keyword_search(part_list[i]) as parameter
        urls = get_url(info_json) # Function from dk_keyword_buy_info.py
        link.append(urls)
        if urls != None: # URL exists
            Supplier.append("DigiKey")
            a_qty_buy.append(None)
        else: # No URL
            Notes.append(None)
            Supplier.append(None)
            a_qty_buy.append(None)
        
        mounting_case = get_case_mountingType(info_json) # Function from dk_keyword_buy_info.py; mounting_case tuple contains package/case and mounting type
        packageSize.append(mounting_case[0])
        mountingType.append(mounting_case[1])
        n_termination = get_number_terminations(info_json) # Function from dk_keyword_buy_info.py
        n_termination_list.append(n_termination)
        
        lead_time = get_leadtime(info_json) # Function from dk_keyword_buy_info.py
        leadtime.append(lead_time)
        
        QOH = get_QOH(info_json) # Function from dk_keyword_buy_info.py
        qty_available.append(QOH)
        if qty_available[i] == None: # No info on QOH
            # if leadtime[i] == "No lead time information available":
            if urls != None:
                Notes.append("Please Check URL")
            unit_price.append(None)
            ext.append(None)
            excess.append(None)
            try:
                qty_b1_unit_price.append(None)
                qty_b1_ext.append(None)
                qty_b1_excess.append(None)
            except NameError:
                pass
            try:
                qty_b2_unit_price.append(None)
                qty_b2_ext.append(None)
                qty_b2_excess.append(None)
            except NameError:
                pass
            try:
                qty_b3_unit_price.append(None)
                qty_b3_ext.append(None)
                qty_b3_excess.append(None)
            except NameError:
                pass
            try:
                qty_b4_unit_price.append(None)
                qty_b4_ext.append(None)
                qty_b4_excess.append(None)
            except NameError:
                pass
            try:
                qty_b5_unit_price.append(None)
                qty_b5_ext.append(None)
                qty_b5_excess.append(None)
            except NameError:
                pass
            continue
        elif qty_available[i] == 0: # No in stock
            Notes.append("No Stock")
        elif qty_available[i] < qty_buy_list[i]: # Not Enough Stock
            Notes.append("Not Enough Stock")
        # elif qty_available[i] >= qty_buy_list[i]:
        #     Notes.append(None)
            
        pricing = get_price_exact(info_json, qty_buy_list[i]) # Function from dk_keyword_buy_info.py; pricing tuple contains qty buy, unit price, ext
        unit_price.append(pricing[1])
        ext.append(pricing[2])
        # excess.append(pricing[2]-(pricing[1]*qty_need_list[i]))
        if pricing[1] == None:
            excess.append(None)
        else:
            excess.append(pricing[2]-(pricing[1]*qty_need_list[i]))
        if qty_available[i] >= qty_buy_list[i]: # More or Enough stock
            if pricing[1] == None and pricing[2] == None: # No pricing
                Notes.append("Please Check URL")
            else:
                Notes.append(None)
        # If the sheet1 qty order 1, 2, 3, 4, 5 is filled; use get_price_exact funtion
        try:
            pricing_b1 = get_price_exact(info_json, qty_b1_buy_list[i])
            qty_b1_unit_price.append(pricing_b1[1])
            qty_b1_ext.append(pricing_b1[2])
            qty_b1_excess.append(pricing_b1[2]-(pricing_b1[1]*qty_b1_list[i]))
        except NameError:
            pass
        try:
            pricing_b2 = get_price_exact(info_json, qty_b2_buy_list[i])
            qty_b2_unit_price.append(pricing_b2[1])
            qty_b2_ext.append(pricing_b2[2])
            qty_b2_excess.append(pricing_b2[2]-(pricing_b2[1]*qty_b2_list[i]))
        except NameError:
            pass
        try:
            pricing_b3 = get_price_exact(info_json, qty_b3_buy_list[i])
            qty_b3_unit_price.append(pricing_b3[1])
            qty_b3_ext.append(pricing_b3[2])
            qty_b3_excess.append(pricing_b3[2]-(pricing_b3[1]*qty_b3_list[i]))
        except NameError:
            pass
        try:
            pricing_b4 = get_price_exact(info_json, qty_b4_buy_list[i])
            qty_b4_unit_price.append(pricing_b4[1])
            qty_b4_ext.append(pricing_b4[2])
            qty_b4_excess.append(pricing_b4[2]-(pricing_b4[1]*qty_b4_list[i]))
        except NameError:
            pass
        try:
            pricing_b5 = get_price_exact(info_json, qty_b5_buy_list[i])
            qty_b5_unit_price.append(pricing_b5[1])
            qty_b5_ext.append(pricing_b5[2])
            qty_b5_excess.append(pricing_b5[2]-(pricing_b5[1]*qty_b5_list[i]))
        except NameError:
            pass
    # Add list to df
    df['Unit Price'] = unit_price
    df['Ext'] = ext
    df['Excess'] = excess
    df['Lead Time'] = leadtime
    df['Q O H'] = qty_available
    df['Notes'] = Notes
    df['Supplier'] = Supplier
    df['Mounting Type'] = mountingType
    df['Package/Case'] = packageSize
    df['Terminations'] = n_termination_list
    df['TTI Min Buy Qty'] = a_qty_buy
    try:
        df['Q1 Need'] = qty_b1_list
        df['Q1 Buy'] = qty_b1_buy_list
        df['Q1 Unit Price'] = qty_b1_unit_price
        df['Q1 Ext'] = qty_b1_ext
        df['Q1 Excess'] = qty_b1_excess
    except NameError:
        pass
    try:
        df['Q2 Need'] = qty_b2_list
        df['Q2 Buy'] = qty_b2_buy_list
        df['Q2 Unit Price'] = qty_b2_unit_price
        df['Q2 Ext'] = qty_b2_ext
        df['Q2 Excess'] = qty_b2_excess
    except NameError:
        pass
    try:
        df['Q3 Need'] = qty_b3_list
        df['Q3 Buy'] = qty_b3_buy_list
        df['Q3 Unit Price'] = qty_b3_unit_price
        df['Q3 Ext'] = qty_b3_ext
        df['Q3 Excess'] = qty_b3_excess
    except NameError:
        pass
    try:
        df['Q4 Need'] = qty_b4_list
        df['Q4 Buy'] = qty_b4_buy_list
        df['Q4 Unit Price'] = qty_b4_unit_price
        df['Q4 Ext'] = qty_b4_ext
        df['Q4 Excess'] = qty_b4_excess
    except NameError:
        pass
    try:
        df['Q5 Need'] = qty_b5_list
        df['Q5 Buy'] = qty_b5_buy_list
        df['Q5 Unit Price'] = qty_b5_unit_price
        df['Q5 Ext'] = qty_b5_ext
        df['Q5 Excess'] = qty_b5_excess
    except NameError:
        pass
    df['URL'] = link
    df = df.style.apply(highlight_row, axis=None) # any df been modified by df.styling can only pass data through df.data
    # Save to Excel sheet
    with pd.ExcelWriter(path, mode = "a", engine = 'openpyxl', if_sheet_exists = "new") as writer:
        df.to_excel(writer, sheet_name='DK_Results', index=False)
    return df.data

"""TEST CASE"""
# if __name__ == "__main__":
#     path = r"C:\Users\Lan\Documents\bom_quoter\BOM-sample\05-072889-01-a-test.xlsx"
#     start_time = time.time()
#     results = dk_get_result(path)
#     print("--- %s seconds ---" % (time.time() - start_time))