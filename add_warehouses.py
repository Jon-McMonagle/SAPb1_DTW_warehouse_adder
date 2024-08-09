#!/usr/bin/python3

import pandas as pd
import time
import os
from os import listdir
from os.path import isfile
import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename
from datetime import date


'''
This program reads an xlsx file or csv and looks for 3
columns: Items, Lines, and Warehouses.
It will then ask which warehouses you want added in a space separated list.
Once it is complete it will save it as a csv that is ready to be uploaded to
the SAP B1 DTW (data transfer workbench).
'''



def main():
    ''' Variable initalization '''
    index1 = 0  # starting point for next sublist of items to add code to
    index2 = 0  # ending point for sublist of items to add code to
    ' All 3 of the below lists should be the same length '
    item_list = []  # item list for converting back to csv
    til = []        # temp item list to append to main list 
    line_list = []  # line list for converting back to csv
    tll = []        # temp line list to append to main list
    whs_list = []   # warehouse list for converting back to csv
    twl = []        # temp warehouse list to append to main list    

    ''' Get folder to save to and working file '''

    print("Select a folder to save to")
    time.sleep(1)
    path = askdirectory(title='Select folder to save to')
    os.chdir(path)
    print("Select initial file")
    time.sleep(1)
    file = askopenfilename(title='Select file to use')
    if file.endswith('.xlsx'):
        items_df, lines_df, whs_df = read_xlsx(file)
    elif file.endswith('.csv'):
        items_df, lines_df, whs_df = read_csv(file)

    items = items_df.tolist()
    lines = lines_df.tolist()
    whs = whs_df.tolist()
    item_count = len(items)

    raw_input = input("Enter space separated list of warehouses to add: ")
    warehouses = list(map(str, raw_input.split()))

    for i in range(0, len(warehouses)):
        whs_to_add = warehouses[i]
        item_list = []
        line_list = []
        whs_list = []
        while index1 < item_count:
            index2 = get_indexes(items,index1)
            til, twl, tll = add_values(index1, index2, items, lines, whs, whs_to_add)
            item_list.extend(til)
            line_list.extend(tll)
            whs_list.extend(twl)
            index1 = index2+1
        # reset the parameters for adding next warehouse
        index1 = 0
        index2 = 0
        items = item_list
        lines = line_list
        whs = whs_list
        item_count = len(items)

    'combine the three lists into one dataframe and then write the df to csv'
    #try:
    write_to_csv(item_list,line_list,whs_list)
    #except: print("Error occurred writing to csv... Exiting")
  


def read_xlsx(file):
    sheet = pd.read_excel(file, index_col=None)
    items = sheet.iloc[:,0]
    lines = sheet.iloc[:,1]
    whs_code = sheet.iloc[:,2]
    return(items,lines,whs_code)



def read_csv(file):
    sheet = pd.read_csv(file, index_col=None)
    items = sheet.iloc[:,0]
    lines = sheet.iloc[:,1]
    whs_code = sheet.iloc[:,2]
    return(items,lines,whs_code)



'''
This function finds the last index where the starting item
matches the ending item
'''
def get_indexes(items,index1):
    count = index1
    item1 = items[index1]
    item2 = item1
    while item1 == item2:
        try:
            count += 1
            item2 = items[count]
        except:
            break
    index2 = count-1
    return(index2)



'''
This function takes two indexes, adds an extra item to the list, adds
the warehouse to the list, and adds an extra number
to the line list. It then returns all 3 lists to be appended to the main
lists.
'''
def add_values(in1, in2, items, lines, whs, whs_to_add):
    # item list
    til = items[in1:in2+1]
    til.append(items[in1])
    # whs list
    twl = list(map(str, whs[in1:in2+1]))
    twl.append(whs_to_add)
    # line list
    tll = lines[in1:in2+1]
    newline = int(lines[in2]+1)
    tll.append(newline)
    return(til,twl,tll)



def write_to_csv(il,ll,wl):
    df = pd.DataFrame({'ParentKey':il, 'LineNum':ll, 'WarehouseCode':wl})
    dtw_row = pd.DataFrame({'ParentKey':'ItemCode', 'LineNum':'LineNum',
                            'WarehouseCode':'WhsCode'}, index=[0])
    df = pd.concat([dtw_row, df]).reset_index(drop = True)
    df.set_index('ParentKey', inplace=True)
    filename = input("Enter a name for the file: ")
    df.to_csv(filename+'.csv', sep=',', encoding = 'utf-8')
    
    

if __name__ == '__main__':
    print("Please ensure columns are in the format: Item No. | Line No. | Whs Code")
    time.sleep(2)
    main()
    print("Program finished. Goodbye :)")
    time.sleep(2)
    
    
