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
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")

def multiprocessing_func(x,url,return_dict):

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
        #print(columntemp["ColumnName"]

    row = data["Rows"]
    df = pd.DataFrame(row)
    for i2 in range(ccount):
        df = df.rename({i2:chead[i2]}, axis='columns')
    dft = dft.append(df)
    print(dft)
    return_dict[x] = url

    return return_dict[x]

if __name__ == '__main__':
    starttime = tt.time()
    node = "DC_WYKO3"
    tools = ['WYKO959','WYKO973','WYKO950','WYKO311','WYKO974','WYKO945']
    today = date.today()
    start = (today - timedelta(days = 1 )).strftime("%m/%d/%Y")
    end = today.strftime("%m/%d/%Y")
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    i = 0
    processes = []
    for tool in tools:
        url = "http://korpimdww018.fact.seagate.com:1520/Metrology_Node/InformationModel/HistorianProvider/ExecuteItem?id=HistorianProvider\WYKO_CR\IMSQL\WYKO\Jermrit_Test\Wyko_AOPTR_Test&node="+node+"&tool="+tool+"&start="+start+"%2000:00:00%20AM&end="+end+"%2000:00:00%20AM"
        p = multiprocessing.Process(target=multiprocessing_func, args=(i,url,return_dict))
        processes.append(p)
        p.start()
        i += 1

    for process in processes:
        process.join()

    #print(return_dict.values())
    
    print('That took {} seconds'.format(tt.time() - starttime))

# %%
