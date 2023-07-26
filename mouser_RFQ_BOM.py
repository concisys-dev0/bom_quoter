from bom_quoter.input_BOM import*
from bom_quoter.mouser_search_buy_info import*
from bom_quoter.df_styling import*
from bom_quoter.mouser_apiKeys import*
import time

"""Return info gather from Mouser API to dataframe and save results to Excel original file as sheet name is Mouser_Results"""
def mouser_get_result(path):
    input_list = setup_BOM_info(path) # Function from input_BOM.py
    # input_list is tuple contains df, part_list, manufacture_list, qty_buy_list, qty_need_list
    df = input_list[0]
    part_list = input_list[1]
    manufacture_list = input_list[2]
    qty_buy_list = input_list[3]
    qty_need_list = input_list[4]
    i = 0
    L = len(part_list) # Length of df (also number of part to be search)
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
    mountingType = []
    packageSize = []
    a_qty_buy = []
    link = []    
    for i in range(L):
        if i % 29 == 0 and i != 0: # rate limit only allow 30 request per minute
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
            mountingType.append(None)
            packageSize.append(None)
            a_qty_buy.append(None)
            link.append(None)
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
            mountingType.append(None)
            packageSize.append(None)
            a_qty_buy.append(None)
            link.append(None)
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
        # print(part_list[i])
        part_json = mouser_SearchByPart(part_list[i]) # Function from mouser_search_v1.py
        if len(part_json['Errors']) != 0: # Error occurs
            err_m = str(part_json['Errors'][0]['Message'])
            print(err_m)
            try: # If daily ratelimit exceeded
                key = change_apiKey_Active(err_m) # Function from mouser_apiKeys.py; ensure change user status and apiKey
                if key != None:
                    print("Change Section API Key to: " + key)
                    part_json = mouser_SearchByPart(part_list[i])
                elif key == None: # Other error
                    return err_m
            except Exception as e:
                raise e
        # Take return of mouser_SearchByPart(part_list[i]) as parameter
        urls = get_url(part_json) # Function from mouser_search_buy_info.py
        link.append(urls)
        if urls != None: # URL exists
            Supplier.append("Mouser")
            mountingType.append(None)
            packageSize.append(None)
            a_qty_buy.append(None)
        else: # No URL
            Supplier.append(None)
            mountingType.append(None)
            packageSize.append(None)
            a_qty_buy.append(None)
            Notes.append(None)
        
        lead_time = get_leadtime(part_json) # Function from mouser_search_buy_info.py
        leadtime.append(lead_time)
        
        QOH = get_QOH(part_json) # Function from mouser_search_buy_info.py
        qty_available.append(QOH)
        if qty_available[i] == None: # No info on QOH
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
        elif qty_available[i] == "0": # No in stock
            Notes.append("No Stock")
        elif int(qty_available[i]) < qty_buy_list[i]: # Not enough stock
            Notes.append("Not Enough Stock")
        # elif int(qty_available[i]) >= qty_buy_list[i]:
        #     Notes.append(None)

        pricing = mouser_get_price(part_json, qty_buy_list[i]) # Function from mouser_search_buy_info.py; pricing tuple contains qty buy, unit price, ext
        unit_price.append(pricing[1])
        ext.append(pricing[2])
        excess.append(pricing[2]-(pricing[1]*qty_need_list[i]))
        if int(qty_available[i]) >= qty_buy_list[i]: # More or Enough stock
            if pricing[1] == None and pricing[2] == None: # No pricing
                Notes.append("Please Check URL")
            else:
                Notes.append(None)
        # If the sheet1 qty order 1, 2, 3, 4, 5 is filled; use mouser_get_price funtion
        try:
            pricing_b1 = mouser_get_price(part_json, qty_b1_buy_list[i])
            qty_b1_unit_price.append(pricing_b1[1])
            qty_b1_ext.append(pricing_b1[2])
            qty_b1_excess.append(pricing_b1[2]-(pricing_b1[1]*qty_b1_list[i]))
        except NameError:
            pass
        try:
            pricing_b2 = mouser_get_price(part_json, qty_b2_buy_list[i])
            qty_b2_unit_price.append(pricing_b2[1])
            qty_b2_ext.append(pricing_b2[2])
            qty_b2_excess.append(pricing_b2[2]-(pricing_b2[1]*qty_b2_list[i]))
        except NameError:
            pass
        try:
            pricing_b3 = mouser_get_price(part_json, qty_b3_buy_list[i])
            qty_b3_unit_price.append(pricing_b3[1])
            qty_b3_ext.append(pricing_b3[2])
            qty_b3_excess.append(pricing_b3[2]-(pricing_b3[1]*qty_b3_list[i]))
        except NameError:
            pass
        try:
            pricing_b4 = mouser_get_price(part_json, qty_b4_buy_list[i])
            qty_b4_unit_price.append(pricing_b4[1])
            qty_b4_ext.append(pricing_b4[2])
            qty_b4_excess.append(pricing_b4[2]-(pricing_b4[1]*qty_b4_list[i]))
        except NameError:
            pass
        try:
            pricing_b5 = mouser_get_price(part_json, qty_b5_buy_list[i])
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
        df.to_excel(writer, sheet_name='Mouser_Results', index=False)
    return df.data

"""TEST CASE"""
# path = r"C:\Users\Lan\Documents\bom_quoter\BOM-sample\05-072889-01-a-test.xlsx"
# start_time = time.time()
# results = mouser_get_result(path)
# print("--- %s seconds ---" % (time.time() - start_time))