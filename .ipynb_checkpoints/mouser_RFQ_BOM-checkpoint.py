from input_BOM import*
from mouser_search_buy_info import*
# get_url, get_leadtime, get_QOH, mouser_get_price
import time

def mouser_get_result(path):
    input_list = setup_BOM_info(path)
    df = input_list[0]
    part_list = input_list[1]
    manufacture_list = input_list[2]
    qty_buy_list = input_list[3]
    qty_need_list = input_list[4]
    i = 0
    L = len(part_list)
    
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
        if i % 29 == 0 and i != 0:
            time.sleep(61)
        """iterate through input list"""
        if part_list[i] == "nan":
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
            continue
        if qty_buy_list[i] == 0:
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
            continue
        
        part_json = mouser_SearchByPart(part_list[i])
        # print(part_json['Errors'])
        if len(part_json['Errors']) != 0:
            print(part_json['Errors'][0]['Message'])
            return None
            break
        
        urls = get_url(part_json)
        link.append(urls)
        if urls != None:
            Supplier.append("Mouser")
            mountingType.append(None)
            packageSize.append(None)
            a_qty_buy.append(None)
        else:
            Supplier.append(None)
            mountingType.append(None)
            packageSize.append(None)
            a_qty_buy.append(None)
            Notes.append(None)
        
        lead_time = get_leadtime(part_json)
        leadtime.append(lead_time)
        
        QOH = get_QOH(part_json)
        qty_available.append(QOH)
        if qty_available[i] == None:
            if urls != None:
                Notes.append("Please Check URL")
            unit_price.append(None)
            ext.append(None)
            excess.append(None)
            continue
        elif qty_available[i] == "0":
            Notes.append("No Stock")
        elif int(qty_available[i]) < qty_buy_list[i]:
            Notes.append("Not Enough Stock")
        elif int(qty_available[i]) >= qty_buy_list[i]:
            Notes.append(None)

        pricing = mouser_get_price(part_json, qty_buy_list[i])
        unit_price.append(pricing[1])
        ext.append(pricing[2])
        excess.append(pricing[2]-(pricing[1]*qty_need_list[i]))

    df['Unit Price'] = unit_price
    df['Ext'] = ext
    df['Excess'] = excess
    df['Lead Time'] = leadtime
    df['Q O H'] = qty_available
    df['Notes'] = Notes
    df['Supplier'] = Supplier
    df['URL'] = link
    df['Mounting Type'] = mountingType
    df['Package/Case'] = packageSize
    df['TTI Min Buy Qty'] = a_qty_buy
    
    with pd.ExcelWriter(path, mode = "a", engine = 'openpyxl', if_sheet_exists = "new") as writer:
        df.to_excel(writer, sheet_name='Mouser_Results', index=False)
    return df

"""TEST CASE"""
# path = r"C:\Users\Lan\Documents\API requests\test doc\RFQ Costed Bom_Wyatt_166177_REV C-RFQtester.xlsx"

# start_time = time.time()
# results = mouser_get_result(path)
# print("--- %s seconds ---" % (time.time() - start_time))