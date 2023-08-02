from pathlib import Path
import pandas as pd
import numpy as np
import time
import sys
import os

"""Summary"""
# Read Excel and save to df
def get_df(path):
    df = pd.read_excel(path, sheet_name = 'Best_Prices', engine ='openpyxl')
    return df

# Return number of items
def get_lines_item(df):
    lines_n = len(df.axes[0])
    return lines_n

# Return number of unknown items price
def get_unknown_items(df):
    # boolean True mean cell is empty
    price_bool = df['Ext'].isna()
    mountType_bool = df['Mounting Type'].isna()
    case_bool = df['Terminations'].isna()
    L = len(df.axes[0]) # length of df
    unknown_i = 0
    for i in range(L):
        if price_bool[i] == True: # and mountType_bool[i] == True
            # if mountType_bool[i] == True and case_bool[i] == True:
            unknown_i = unknown_i + 1
        # elif mountType_bool[i] == True or case_bool[i] == True:
        #     unknown_i = unknown_i + 1
    return unknown_i

# Return Mounting Type and Terminations as list
def list_mounting_terminal(df):
    L = len(df.axes[0]) # length of df
    df['Terminations'].fillna(0, inplace=True) # replace NaN to 0
    mountType_list = []
    terminals_list = []
    for i in range(L):
        mountType = str(df.iloc[i]['Mounting Type'])
        mountType_list.append(mountType)
        terminal = int(df.iloc[i]['Terminations'])
        terminals_list.append(terminal)
    return mountType_list, terminals_list

# Return number of SMT items and total of terminals number
def get_SMT_items(mountType_list, terminals_list):
    l = len(mountType_list) # length of lists
    smt_terminals_list = []
    smt_items_n = 0
    for i in range(l):
        if mountType_list[i] == "SMT":
            smt_terminals_list.append(terminals_list[i]) # list number of terminals
            smt_items_n = smt_items_n + 1
    smt_total_terminals = sum(smt_terminals_list)
    return smt_items_n, smt_total_terminals

# Return number of unknown Terminals of SMT items
def get_unknown_SMT_items(mountType_list, terminals_list):
    l = len(mountType_list) # length of lists
    unknown_smt_n = 0
    for i in range(l):
        if mountType_list[i] == "SMT":
            if terminals_list[i] == 0:
                unknown_smt_n = unknown_smt_n + 1
    return unknown_smt_n
    
# Return number of TH items and total of terminals number
def get_TH_items(mountType_list, terminals_list):
    l = len(mountType_list) # length of lists
    th_terminals_list = []
    th_items_n = 0
    for i in range(l):
        if mountType_list[i] == "TH":
            th_terminals_list.append(terminals_list[i]) # list number of terminals
            th_items_n = th_items_n + 1
    th_total_terminals = sum(th_terminals_list)
    return th_items_n, th_total_terminals

# Return number of unknown Terminals of TH items
def get_unknown_TH_items(mountType_list, terminals_list):
    l = len(mountType_list) # length of lists
    unknown_th_n = 0
    for i in range(l):
        if mountType_list[i] == "TH":
            if terminals_list[i] == 0:
                unknown_th_n = unknown_th_n + 1
    return unknown_th_n

# Return number of MEC items and total of terminals number
def get_MEC_items(mountType_list, terminals_list):
    l = len(mountType_list) # length of lists
    mec_terminals_list = []
    mec_items_n = 0
    for i in range(l):
        if mountType_list[i] == "MEC":
            mec_terminals_list.append(terminals_list[i]) # list number of terminals
            mec_items_n = mec_items_n + 1
    mec_total_terminals = sum(mec_terminals_list)
    return mec_items_n, mec_total_terminals

# Return number of unknown Terminals of MEC items
def get_unknown_MEC_items(mountType_list, terminals_list):
    l = len(mountType_list) # length of lists
    unknown_mec_n = 0
    for i in range(l):
        if mountType_list[i] == "MEC":
            if terminals_list[i] == 0:
                unknown_mec_n = unknown_mec_n + 1
    return unknown_mec_n
# Gather numbers return from the functions, organize them to the df and save to Excel sheet name Summary
def save_summary(path):
    df = get_df(path)
    tt_items = get_lines_item(df) # number of total items
    unknown_items = get_unknown_items(df) # number of unknown price items
    
    mt_list = list_mounting_terminal(df) # get list of mounting type & terminal
    mountType_list = mt_list[0]
    terminals_list = mt_list[1]
    
    smt = get_SMT_items(mountType_list, terminals_list)
    smt_items_n = smt[0] # number of total SMT items
    smt_total_terminals = smt[1] # total SMT terminals
    unknown_smt_n = get_unknown_SMT_items(mountType_list, terminals_list) # number of SMT items unknown terminals

    th = get_TH_items(mountType_list, terminals_list)
    th_items_n = th[0] # number of total TH items
    th_total_terminals = th[1] # total TH terminals
    unknown_th_n = get_unknown_TH_items(mountType_list, terminals_list) # number of TH items unknown terminals

    mec = get_MEC_items(mountType_list, terminals_list)
    mec_items_n = mec[0] # number of total MEC items
    mec_total_terminals = mec[1] # total MEC terminals
    unknown_mec_n = get_unknown_MEC_items(mountType_list, terminals_list) # number of MEC items unkown terminals
    
    val_list = [tt_items, unknown_items, smt_items_n, smt_total_terminals, unknown_smt_n, th_items_n, th_total_terminals, unknown_th_n, mec_items_n, mec_total_terminals, unknown_mec_n] # list of numbers need in summary
    name_list = ["Total Items", "Unknown Price Items", "SMT Items", "SMT Terminals", "Unknown Terminals SMT Items", "TH Items", "TH Terminals", "Unknown Terminals TH Items", "MEC Items", "MEC Terminals", "Unknown Terminals MEC Items"] # list name of the numbers
    df_1 = pd.DataFrame(columns = ['Summary', 'Value']) # create df
    df_1['Summary'] = name_list
    df_1['Value'] = val_list
    with pd.ExcelWriter(path, mode = "a", engine = 'openpyxl', if_sheet_exists = "replace") as writer: # save to Excel
        df_1.to_excel(writer, sheet_name = 'Summary', index = False)
    return df_1

if __name__ == "__main__":
    """TEST CASE"""
    path = r"C:\Users\Lan\Documents\bom_quoter\BOM-sample\05-073194-01-a-test.xlsx"
    print(save_summary(path))