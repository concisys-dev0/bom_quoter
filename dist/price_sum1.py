from pathlib import Path
import pandas as pd
import numpy as np
import time
import sys
import os

"""Price Summary"""
# Read Excel and save to df
def get_df(path):
    df = pd.read_excel(path, sheet_name = 'Best_Prices', engine ='openpyxl')
    return df
    
# Alert when the BOM not fill Terminals column full
def empty_warning(df):
    bool_empty = df['Terminations'].isna()
    for i in range(len(bool_empty)):
        if bool_empty[i] == True:
            print("The program cannot continue, empty elements in Terminations")
            return None
    return "OK"
    
# Material price of Qty Order
def price_sum_ext(path):
    df = get_df(path)
    df['Ext'].fillna(0, inplace=True) # replace NaN to 0
    sum_ext = float(df['Ext'].sum())
    return sum_ext

# Material price of Qty Order 1
def price_sum_Q1ext(path):
    df = get_df(path)
    df['Q1 Ext'].fillna(0, inplace=True) # replace NaN to 0
    sum_Q1ext = float(df['Q1 Ext'].sum())
    return sum_Q1ext

# Material price of Qty Order 2
def price_sum_Q2ext(path):
    df = get_df(path)
    df['Q2 Ext'].fillna(0, inplace=True) # replace NaN to 0
    sum_Q2ext = float(df['Q2 Ext'].sum())
    return sum_Q2ext

# Material price of Qty Order 3
def price_sum_Q3ext(path):
    df = get_df(path)
    df['Q3 Ext'].fillna(0, inplace=True) # replace NaN to 0
    sum_Q3ext = float(df['Q3 Ext'].sum())
    return sum_Q3ext

# Material price of Qty Order 4
def price_sum_Q4ext(path):
    df = get_df(path)
    df['Q4 Ext'].fillna(0, inplace=True) # replace NaN to 0
    sum_Q4ext = float(df['Q4 Ext'].sum())
    return sum_Q4ext

# Material price of Qty Order 5
def price_sum_Q5ext(path):
    df = get_df(path)
    df['Q5 Ext'].fillna(0, inplace=True) # replace NaN to 0
    sum_Q5ext = float(df['Q5 Ext'].sum())
    return sum_Q5ext

# Price 1 board base on unit price
def price_1B(path):
    df = get_df(path)
    df['Unit Price'].fillna(0, inplace=True) # replace NaN to 0
    df['Quantity'].fillna(0, inplace=True)
    parts_price = df['Quantity']*df['Unit Price']
    # print(parts_price)
    board_price = sum(parts_price)
    print(board_price)
    return board_price

# Total SMT terminals number
def price_labor_SMT(path, order):
    df = get_df(path)
    L = len(df.axes[0]) # length of df
    qty_list = []
    mountType_list = []
    terminals_list = []
    for i in range(L):
        qty = int(df.iloc[i]['Quantity'])
        qty_list.append(qty)
        mountType = str(df.iloc[i]['Mounting Type'])
        mountType_list.append(mountType)
        terminal = int(df.iloc[i]['Terminations'])
        terminals_list.append(terminal)

    l = len(qty_list) # length of lists
    smt_terminals_list = []
    for i in range(l):
        if mountType_list[i] == "SMT":
            smt_terminals = terminals_list[i]# number of terminals per board for 1 item
            smt_terminals_list.append(smt_terminals)
    # print(smt_terminals_list)
    # total number of terminals from order value
    smt_total_terminals = sum(smt_terminals_list) # total number of terminals per board 
    smt_terminals_order = smt_total_terminals*order # total number of terminals follow qty order
    return smt_terminals_order

# Total TH terminals number
def price_labor_TH(path, order):
    df = get_df(path)
    L = len(df.axes[0]) # length of df
    qty_list = []
    mountType_list = []
    terminals_list = []
    for i in range(L):
        qty = int(df.iloc[i]['Quantity'])
        qty_list.append(qty)
        mountType = str(df.iloc[i]['Mounting Type'])
        mountType_list.append(mountType)
        terminal = int(df.iloc[i]['Terminations'])
        terminals_list.append(terminal)

    l = len(qty_list) # length of lists
    th_terminals_list = []
    for i in range(l):
        if mountType_list[i] == "TH":
            th_terminals = terminals_list[i]*qty_list[i] # number of terminals per board for 1 item
            th_terminals_list.append(th_terminals)
    # total number of terminals from order value
    th_total_terminals = sum(th_terminals_list) # total number of terminals per board 
    th_terminals_order = th_total_terminals*order # total number of terminals follow qty order
    return th_terminals_order

# Total MEC terminals number
def price_labor_MEC(path, order):
    df = get_df(path)
    L = len(df.axes[0]) # length of df
    qty_list = []
    mountType_list = []
    terminals_list = []
    for i in range(L):
        qty = int(df.iloc[i]['Quantity'])
        qty_list.append(qty)
        mountType = str(df.iloc[i]['Mounting Type'])
        mountType_list.append(mountType)
        terminal = int(df.iloc[i]['Terminations'])
        terminals_list.append(terminal)

    l = len(qty_list) # length of lists
    mec_terminals_list = []
    for i in range(l):
        if mountType_list[i] == "MEC":
            mec_terminals = terminals_list[i]*qty_list[i] # number of terminals per board for 1 item
            mec_terminals_list.append(mec_terminals)
    # print(mec_terminals_list)
    # total number of terminals from order value
    mec_total_terminals = sum(mec_terminals_list) # total number of terminals per board 
    mec_terminals_order = mec_total_terminals*order # total number of terminals follow qty order
    return mec_terminals_order

# Return the df of Price Summary
def df_summary(path):
    df = get_df(path)
    condition_met = empty_warning(df)
    if condition_met != "OK": # check if Terminals column is empty
        return df
    df_s1 = pd.read_excel(path, sheet_name = 'Sheet1', engine ='openpyxl')
    df_s1['Qty'].fillna(0, inplace=True) # replace NaN to 0
    order_list = []
    for i in range(len(df_s1.axes[0])): # get the Qty list
        orders = int(df_s1.iloc[i]['Qty'])
        order_list.append(orders)
    # Calculate the total Material Prices
    sum_oext = [None]*6 # Holding initial
    sum_oext[0] = price_sum_ext(path)
    if order_list[1] != 0:
        sum_oext[1] = price_sum_Q1ext(path)
    else:
        sum_oext[1] = 0
    if order_list[2] != 0:
        sum_oext[2] = price_sum_Q2ext(path)
    else:
        sum_oext[2] = 0
    if order_list[3] != 0:
        sum_oext[3] = price_sum_Q3ext(path)
    else:
        sum_oext[3] = 0
    if order_list[4] != 0:
        sum_oext[4] = price_sum_Q4ext(path)
    else:
        sum_oext[4] = 0
    if order_list[5] != 0:
        sum_oext[5] = price_sum_Q5ext(path)
    else:
        sum_oext[5] = 0
    
    l = len(order_list)
    SMT_terminals = []
    SMT_labor_price = []
    TH_terminals = []
    TH_labor_price = []
    MEC_terminals = []
    MEC_labor_price = []
    total_labor_price = []
    for i in range(l):
        smt_tt = price_labor_SMT(path, order_list[i])
        SMT_terminals.append(smt_tt)
        smt_labor_price = smt_tt*smt_labor_c
        SMT_labor_price.append(smt_labor_price)
        
        th_tt = price_labor_TH(path, order_list[i])
        TH_terminals.append(th_tt)
        th_labor_price = th_tt*th_labor_c
        TH_labor_price.append(th_labor_price)
        
        mec_tt = price_labor_MEC(path, order_list[i])
        MEC_terminals.append(mec_tt)
        mec_labor_price = mec_tt*mec_labor_c
        MEC_labor_price.append(mec_labor_price)

        total = smt_labor_price + th_labor_price + mec_labor_price
        total_labor_price.append(total)
        
    df_s1['Material Price'] = sum_oext
    df_s1['SMT terminals'] = SMT_terminals
    df_s1['TH Terminals'] = TH_terminals
    df_s1['MEC Terminals'] = MEC_terminals
    df_s1['SMT Labor Price'] = SMT_labor_price
    df_s1['TH Labor Price'] = TH_labor_price
    df_s1['MEC Labor Price'] = MEC_labor_price
    df_s1['Total Labor Price'] = total_labor_price
    return df_s1

# Save the df result to Excel
def save_summary(path):
    df = df_summary(path)
    print(df)
    with pd.ExcelWriter(path, mode = "a", engine = 'openpyxl', if_sheet_exists = "new") as writer:
        df.to_excel(writer, sheet_name = 'Summary', index = False)
    return df

"""TEST CASE"""
smt_labor_c = 0.5
th_labor_c = 1
mec_labor_c = 1.15
start_time = time.time()
path = r"C:\Users\Lan\Documents\TestBOMs\42790 BOM V 0004  - PN 42910 Rev 2-test.xlsx"
save_summary(path)
print("----- %s seconds -----" % (time.time() - start_time))