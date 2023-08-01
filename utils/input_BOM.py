import pandas as pd
import numpy as np
import openpyxl
from openpyxl import load_workbook

"""Setup the lists and df"""
# Calculate the qty need for each Qty Order # in Sheet1
def calculate_needQty(path):
    df = pd.read_excel(path, sheet_name = 'Sheet1', engine='openpyxl')
    df2 = pd.read_excel(path, sheet_name = 'BOM', engine='openpyxl')
        
    a = pd.isnull(df['Qty'].iloc[0]) # Type boolean cell empty is True
    if a == False:
        df2['Qty Need'] = (df['Qty'].iloc[0])*df2['Quantity']
        df2['Qty Need'].fillna(0, inplace=True) # replace NaN to 0
    b = pd.isnull(df['Qty'].iloc[1])
    if b == False:
        df2['Q1 Need'] = (df['Qty'].iloc[1])*df2['Quantity']
        df2['Q1 Need'].fillna(0, inplace=True) # replace NaN to 0
    c = pd.isnull(df['Qty'].iloc[2])
    if c == False:
        df2['Q2 Need'] = (df['Qty'].iloc[2])*df2['Quantity']
        df2['Q2 Need'].fillna(0, inplace=True) # replace NaN to 0
    d = pd.isnull(df['Qty'].iloc[3])
    if d == False:
        df2['Q3 Need'] = (df['Qty'].iloc[3])*df2['Quantity']
        df2['Q3 Need'].fillna(0, inplace=True) # replace NaN to 0
    e = pd.isnull(df['Qty'].iloc[4])
    if e == False:
        df2['Q4 Need'] = (df['Qty'].iloc[4])*df2['Quantity']
        df2['Q4 Need'].fillna(0, inplace=True) # replace NaN to 0
    f = pd.isnull(df['Qty'].iloc[5])
    if f == False:
        df2['Q5 Need'] = (df['Qty'].iloc[4])*df2['Quantity']
        df2['Q5 Need'].fillna(0, inplace=True) # replace NaN to 0
        
    with pd.ExcelWriter(path, mode = "a", engine = 'openpyxl', if_sheet_exists = "replace") as writer:
        df2.to_excel(writer, sheet_name = 'BOM', index = False)
    return df2

# Gather info need into list and pass BOM to df
def setup_BOM_info(path):
    r_df = calculate_needQty(path)
    # workbook enable read value from formulas, just need to make sure they're correct format data type in Excel
    # wb = load_workbook(filename=path , data_only=True) #
    # ws = wb['BOM'] # .get_sheet_by_name(name='')
    # wb.save(path)
    # wb.close()
    # df = pd.DataFrame(ws.values)
    df = pd.read_excel(path, sheet_name = 'BOM')
    # df = pd.read_excel(workbook, sheet_name = 'BOM', engine='openpyxl')
    start_rowI = df[df.eq("Manufacturer Part Number").any(axis=1)].index.to_numpy() # make sure the df start at correct header row
    if start_rowI.size >= 1:
        start_row = start_rowI[0]
        df_BOM = df.iloc[start_row+1:]
        df_BOM.columns = df.iloc[start_row]
    else:
        df_BOM = df.iloc[0:]
    # initial list
    part_list = []
    manufacture_list = []
    qty_need_list = []
    qty_buy_list = []
    L = len(df_BOM.axes[0]) # length of df
    for i in range(L):
        part_id = str(df_BOM.iloc[i]['Manufacturer Part Number'])
        part_list.append(part_id)
        manufacture = str(df_BOM.iloc[i]['Manufacturer'])
        manufacture_list.append(manufacture)
        qty_need = int(df_BOM.iloc[i]['Qty Need'])
        qty_need_list.append(qty_need)
        qty_buy= int(df_BOM.iloc[i]['Qty Buy'])
        qty_buy_list.append(qty_buy)
    # Checking if pandas able to read data from Excel
    # print(part_list)
    # print(manufacture_list)
    # print(qty_need_list)
    # print(qty_buy_list)
    # If any Qty Order 1, 2, 3, 4, 5 exists
    if 'Q1 Need' in df_BOM.columns:
        qty_b1_list = []
        qty_b1_buy_list = []
        for a in range(L):
            qty_b1 = int(df_BOM.iloc[a]['Q1 Need'])
            qty_b1_list.append(qty_b1)
            qty_b1_buy = int(df_BOM.iloc[a]['Q1 Buy'])
            qty_b1_buy_list.append(qty_b1_buy)
        if 'Q2 Need' not in df_BOM.columns:
            return df_BOM, part_list, manufacture_list, qty_buy_list, qty_need_list, qty_b1_list, qty_b1_buy_list
    if "Q2 Need" in df_BOM.columns:
        qty_b2_list = []
        qty_b2_buy_list = []
        for b in range(L):
            qty_b2 = int(df_BOM.iloc[b]['Q2 Need'])
            qty_b2_list.append(qty_b2)
            qty_b2_buy = int(df_BOM.iloc[b]['Q2 Buy'])
            qty_b2_buy_list.append(qty_b2_buy)
        if "Q3 Need" not in df_BOM.columns:
            return df_BOM, part_list, manufacture_list, qty_buy_list, qty_need_list, qty_b1_list, qty_b1_buy_list, qty_b2_list, qty_b2_buy_list
    if "Q3 Need" in df_BOM.columns:
        qty_b3_list = []
        qty_b3_buy_list = []
        for c in range(L):
            qty_b3 = int(df_BOM.iloc[c]['Q3 Need'])
            qty_b3_list.append(qty_b3)
            qty_b3_buy = int(df_BOM.iloc[c]['Q3 Buy'])
            qty_b3_buy_list.append(qty_b3_buy)
        if "Q4 Need" not in df_BOM.columns:
            return df_BOM, part_list, manufacture_list, qty_buy_list, qty_need_list, qty_b1_list, qty_b1_buy_list, qty_b2_list, qty_b2_buy_list, qty_b3_list, qty_b3_buy_list
    if "Q4 Need" in df_BOM.columns:
        qty_b4_list = []
        qty_b4_buy_list = []
        for d in range(L):
            qty_b4 = int(df_BOM.iloc[d]['Q4 Need'])
            qty_b4_list.append(qty_b4)
            qty_b4_buy = int(df_BOM.iloc[d]['Q4 Buy'])
            qty_b4_buy_list.append(qty_b4_buy)
        if "Q5 Need" not in df_BOM.columns:
            return df_BOM, part_list, manufacture_list, qty_buy_list, qty_need_list, qty_b1_list, qty_b1_buy_list, qty_b2_list, qty_b2_buy_list, qty_b3_list, qty_b3_buy_list, qty_b4_list, qty_b4_buy_list
    if "Q5 Need" in df_BOM.columns:
        qty_b5_list = []
        qty_b5_buy_list = []
        for e in range(L):
            qty_b5 = int(df_BOM.iloc[e]['Q5 Need'])
            qty_b5_list.append(qty_b5)
            qty_b5_buy = int(df_BOM.iloc[e]['Q5 Buy'])
            qty_b5_buy_list.append(qty_b5_buy)
        return df_BOM, part_list, manufacture_list, qty_buy_list, qty_need_list, qty_b1_list, qty_b1_buy_list, qty_b2_list, qty_b2_buy_list, qty_b3_list, qty_b3_buy_list, qty_b4_list, qty_b4_buy_list, qty_b5_list, qty_b5_buy_list
    
    return df_BOM, part_list, manufacture_list, qty_buy_list, qty_need_list

"""TEST CASE"""
# path = r"C:\Users\Lan\Documents\bom_quoter\BOM-sample\05-072889-01-a-test.xlsx"
# df_r = setup_BOM_info(path)
# print(df_r[0].head(5))