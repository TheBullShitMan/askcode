#%%
import pandas as pd
import time as tt
import multiprocessing 
import logging
import numpy as np
import requests
import matplotlib.pyplot as plt
import seaborn as sb
sb.set_style('whitegrid')
from datetime import date, time, datetime, timedelta
from threading import Thread 

def multiprocessing_func(url):

    df = pd.DataFrame()

    response = requests.get(url)
    rawdata = response.json()

    data = rawdata["Results"][0]['Data']

    ccount = data["ColumnsCount"]
    column = data["Columns"]

    chead = []
    for i in range(ccount):
        columntemp = column[i]
        chead.append(columntemp["ColumnName"])

    row = data["Rows"]
    df = pd.DataFrame(row)
    for i2 in range(ccount):
        df = df.rename({i2:chead[i2]}, axis='columns')

    return df

if __name__ == '__main__':
    starttime = tt.time()
    node = "DC_WYKO3"
    tools = ['WYKO959','WYKO973','WYKO950','WYKO311','WYKO974','WYKO945']
    today = date.today()
    start = (today - timedelta(days = 1 )).strftime("%m/%d/%Y")
    end = today.strftime("%m/%d/%Y")
    manager = multiprocessing.Manager()
    processes = []
    for tool in tools:
        url = "URLของJSON"
        p = multiprocessing.Process(target=multiprocessing_func, args=(url))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()
        

    
    print('That took {} seconds'.format(tt.time() - starttime))

# %%
