import pandas as pd
import numpy as np
import openpyxl
from openpyxl import load_workbook

def setup_BOM_info(path):
    wb = load_workbook(filename=path , data_only=True) #
    ws = wb['BOM'] # .get_sheet_by_name(name='')
    wb.save(path)
    wb.close()
    df = pd.DataFrame(ws.values)
    # workbook enable read value from formulas, just need to make sure they're correct format data type in Excel
    # df = pd.read_excel(workbook, sheet_name = 'BOM', engine='openpyxl')
    start_rowI = df[df.eq("Manufacturer Part Number").any(axis=1)].index.to_numpy()
    # make sure the df start at correct header
    if start_rowI.size >= 1:
        start_row = start_rowI[0]
        df_BOM = df.iloc[start_row+1:]
        df_BOM.columns = df.iloc[start_row]
    else:
        df_BOM = df.iloc[0:]
        
    part_list = []
    manufacture_list = []
    qty_need_list = []
    qty_buy_list = []
    # length of df
    L = len(df_BOM.axes[0])
    for i in range(L):
        part_id = str(df_BOM.iloc[i]['Manufacturer Part Number'])
        part_list.append(part_id)
        manufacture = str(df_BOM.iloc[i]['Manufacturer'])
        manufacture_list.append(manufacture)
        qty_need = df_BOM.iloc[i]['Qty Need']
        qty_need_list.append(qty_need)
        qty_buy= df_BOM.iloc[i]['Qty Buy']
        qty_buy_list.append(qty_buy)
    # checking if pandas able to read data from Excel
    # print(part_list)
    # print(manufacture_list)
    # print(qty_need_list)
    # print(qty_buy_list)
    
    return df_BOM, part_list, manufacture_list, qty_buy_list, qty_need_list

"""TEST CASE"""
# path = r"C:\Users\Lan\Documents\API requests\test doc\BOM-PCA_Optics_Test_Tool_Main_216673(DEV)-RFQtester.xlsx"
# df_r = setup_BOM_info(path)
# print(df_r[0].tail(7))