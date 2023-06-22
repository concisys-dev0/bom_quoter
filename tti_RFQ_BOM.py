from tti_search_buy_info import*
from input_BOM import*
import time

def tti_get_result(path):
    input_list = setup_BOM_info(path)
    df = input_list[0]
    part_list = input_list[1]
    manufacture_list = input_list[2]
    qty_buy_list = input_list[3]
    qty_need_list = input_list[4]
    i = 0
    L = len(part_list)
    
    a_qty_buy = []
    unit_price = []
    ext = []
    excess = []
    leadtime = []
    Notes = [] # [None]*L
    qty_available = []
    Supplier =[]
    mountingType = []
    packageSize = []
    link = []
    
    for i in range(L):
        """iterate through input list"""
        if part_list[i] == "nan":
            a_qty_buy.append(None)
            unit_price.append(None)
            ext.append(None)
            excess.append(None)
            leadtime.append(None)
            Notes.append(None)
            qty_available.append(None)
            Supplier.append(None)
            mountingType.append(None)
            packageSize.append(None)
            link.append(None)
            continue
        if qty_buy_list[i] == 0:
            a_qty_buy.append(None)
            unit_price.append(None)
            ext.append(None)
            excess.append(None)
            leadtime.append(None)
            Notes.append(None)
            qty_available.append(None)
            Supplier.append(None)
            mountingType.append(None)
            packageSize.append(None)
            link.append(None)
            continue
        
        # print(part_list[i])    
        info_json = tti_SearchByKeyword(part_list[i])
        if 'recordCount' in info_json and info_json['recordCount'] == 0:
            # print("The part is not available please try another supplier. ")
            a_qty_buy.append(None)
            unit_price.append(None)
            ext.append(None)
            excess.append(None)
            leadtime.append(None)
            Notes.append(None)
            qty_available.append(None)
            Supplier.append(None)
            mountingType.append(None)
            packageSize.append(None)
            link.append(None)
            continue
        elif 'code' in info_json:
            print(info_json['code'] + ": " + info_json['message'])
            continue
            
        urls = get_url(info_json)
        link.append(urls)
        if urls != None:
            Supplier.append("TTI")
            mountingType.append(None)
        else:
            Supplier.append(None)
            mountingType.append(None)
            Notes.append(None)
            
        case = get_case_mountingType(info_json)
        packageSize.append(case)
            
        lead_time = get_leadtime(info_json)
        leadtime.append(lead_time)
        if leadtime == "Contact TTI":
            Notes.append("Contact TTI")
        
        QOH = get_QOH(info_json)
        qty_available.append(QOH)
        if QOH == None:
            if urls != None:
                Notes.append("Please check URL")
            a_qty_buy.append(None)
            unit_price.append(None)
            ext.append(None)
            excess.append(None)
            continue
        elif QOH == 0:
            Notes.append("No Stock")
        elif int(QOH) < qty_buy_list[i]:
            Notes.append("Not Enough Stock")
        elif int(QOH) >= qty_buy_list[i]:
            Notes.append(None)
            
        pricing = get_price(info_json, qty_buy_list[i])
        a_qty_buy.append(pricing[0])
        unit_price.append(pricing[1])
        ext.append(pricing[2])
        if pricing[1] == None:
            excess.append(None)
        else:
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
        df.to_excel(writer, sheet_name = 'TTI_Results', index = False)
    return df

"""TEST CASE"""
# path = r"C:\Users\Lan\Documents\API requests\test doc\BOM-PCA_Optics_Test_Tool_Main_216673(DEV)-RFQtester.xlsx"

# start_time = time.time()
# results = tti_get_result(path)
# print("--- %s seconds ---" % (time.time() - start_time))