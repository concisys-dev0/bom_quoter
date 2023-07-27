import pandas as pd
import numpy as np
"""Color the text of row that need the PM to modify"""
# Change text of row contain item not in stock, not enough, and need to request
# Used in:dk_RFQ_BOM, mouser_RFQ_BOM, tti_RFQ_BOM, mergeCompare_pricing
def highlight_row(x):
    # Formating change
    c1 = 'color: red; font-weight: bold'
    c2 = 'color: purple; font-weight: bold'
    c3 = 'color: blue; font-weight: bold'
    c = '' # left blank
    # Condition that need change
    m1 = x['Notes'].eq('No Stock')
    m2 = x['Notes'].eq('Not Enough Stock')
    m3 = x['Notes'].eq('Please Check URL')
    m4 = x['Ext'].isna() # where Ext empty cell, mean they can't find the product
    df1 = pd.DataFrame(c, index=x.index, columns=x.columns) # no change
    df1 = df1.mask(m1, c1).mask(m4, c1).mask(m2, c2).mask(m3, c3)
    return df1

# Change text of row contain item not in stock, not enough, need to request, and don't have terminals information
def highlight_noTermimal(x): 
    # Formating change
    c1 = 'color: red; font-weight: bold'
    c2 = 'color: purple; font-weight: bold'
    c3 = 'color: blue; font-weight: bold'
    c4 = 'color: green; font-weight: bold' # Termimals empty cell color
    c = '' # left blank
    # Condition that need change
    m1 = x['Notes'].eq('No Stock')
    m2 = x['Notes'].eq('Not Enough Stock')
    m3 = x['Notes'].eq('Please Check URL')
    m4 = x['Terminations'].isna() # where Termimals empty cell
    m5 = x['Ext'].isna() # where Ext empty cell, mean they can't find the product
    df = pd.DataFrame(c, index=x.index, columns=x.columns) # no change
    df = df.mask(m4, c4).mask(m1, c1).mask(m5, c1).mask(m2, c2).mask(m3, c3)
    return df