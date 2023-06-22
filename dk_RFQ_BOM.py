from dk_keyword_buy_info import*
from input_BOM import*
import time

def dk_get_result(path):
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
    a_qty_buy = []
    mountingType = []
    packageSize = []
    link = []
    n_termination_list = []
    for i in range(L):
        if i % 119 == 0 and i != 0:
            time.sleep(60)
        """iterate through input list"""
        if part_list[i] == "nan":
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
            continue
        if qty_buy_list[i] == 0:
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
            continue
        
        info_json = get_digikey_keyword_search(part_list[i])
        if 'ErrorMessage' in info_json:
            if info_json['ErrorMessage'] == "Daily Ratelimit exceeded":
                print("Daily Ratelimit exceeded; Please try again after 24hrs")
                return None
                break
            else:
                refresh_token_digikey_api()
                info_json = get_digikey_keyword_search(part_list[i])
            
                
        urls = get_url(info_json)
        link.append(urls)
        if urls != None:
            Supplier.append("DigiKey")
            a_qty_buy.append(None)
        else:
            Notes.append(None)
            Supplier.append(None)
            a_qty_buy.append(None)
        
        mounting_case = get_case_mountingType(info_json)
        packageSize.append(mounting_case[0])
        mountingType.append(mounting_case[1])
        n_termination = get_number_terminations(info_json)
        n_termination_list.append(n_termination)
        
        lead_time = get_leadtime(info_json)
        leadtime.append(lead_time)
        
        QOH = get_QOH(info_json)
        qty_available.append(QOH)
        if qty_available[i] == None:
            # if leadtime[i] == "No lead time information available":
            if urls != None:
                Notes.append("Please Check URL")
            unit_price.append(None)
            ext.append(None)
            excess.append(None)
            continue
        elif qty_available[i] == 0:
            Notes.append("No Stock")
        elif qty_available[i] < qty_buy_list[i]:
            Notes.append("Not Enough Stock")
        elif qty_available[i] >= qty_buy_list[i]:
            Notes.append(None)
            
        pricing = get_price_exact(info_json, qty_buy_list[i])
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
    df['Number of Termination'] = n_termination_list
    
    with pd.ExcelWriter(path, mode = "a", engine = 'openpyxl', if_sheet_exists = "new") as writer:
        df.to_excel(writer, sheet_name='DK_Results', index=False)
    return df

"""TEST CASE"""
# path = r"C:\Users\Lan\Documents\API requests\test doc\BOM-PCA_Optics_Test_Tool_Main_216673(DEV)-RFQtester.xlsx"

# start_time = time.time()
# results = dk_get_result(path)
# print("--- %s seconds ---" % (time.time() - start_time))