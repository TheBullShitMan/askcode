#%%
import pandas as pd
import logging
import numpy as np
import time as tt
import requests
import matplotlib.pyplot as plt
import seaborn as sb
import os
sb.set_style('whitegrid')
from datetime import date, time, datetime, timedelta
from threading import Thread 
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")

class get_dataframe(Thread):

    def __init__(self, url,dft):
        Thread.__init__(self)
        self.url = url
        self.dft = dft

    def run(self):

        response = requests.get(self.url)
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
        self.dft = self.dft.append(df)

if(__name__=='__main__'):
    starttime = tt.time()
    node = "DC_WYKO3"
    tools = ['WYKO959','WYKO973','WYKO950','WYKO311','WYKO974','WYKO945']
    today = date.today()
    start = (today - timedelta(days = 1 )).strftime("%m/%d/%Y")
    date_object = datetime.strptime(start,'%m/%d/%Y')
    strt = date_object.strftime('%b%d%y')
    end = today.strftime("%m/%d/%Y")
    date_object = datetime.strptime(end,'%m/%d/%Y')
    ends = date_object.strftime('%b%d%y')
    dft = pd.DataFrame()
    #Start Thread
    threads = []
    for tool in tools:
        url = "URLของJSON"
        thr = get_dataframe(url,dft)
        threads.append(thr)
        thr.start()
    #wait until the end
    for t in threads:
        t.join()
        dft = dft.append(t.dft)
    #Drop Column & Rows unused
    dft = dft.drop(columns=['RunNum', 'ASSY', 'STAGE_ROW', 'STAGE_COL', 'LOT_ID'])
    dft = dft.dropna(subset = ['VIBRATION','INTENSITY','ABS_RA' , 'SNIPPET_CORR'],axis=0)
    
    #Convert date time format
    dft['Timestamp'] = pd.to_datetime(dft.Timestamp)
    dft['Timestamp'] = dft['Timestamp'].dt.strftime('%m-%d-%Y')
    #Data manipulation
    dfm = dft.groupby(['Timestamp','TOOL','PRODUCT','RUN_NUM'])['VIBRATION','INTENSITY','ABS_RA' , 'SNIPPET_CORR'].mean()
    dfs = dft.groupby(['Timestamp','TOOL','PRODUCT','RUN_NUM'])['VIBRATION','INTENSITY','ABS_RA' , 'SNIPPET_CORR'].std()
    dff = pd.merge(dfm,dfs, on=['Timestamp',"TOOL",'PRODUCT','RUN_NUM'])
    #export to csv
    dft.to_csv(r'C:\Users\743670\Desktop\test\project\rawdata.csv')
    f_name = r'\DC_WYKO3' +strt + '_' + ends + '.csv'
    path = r'C:\Users\743670\Desktop\test\project'
    pather = path + '' + f_name
    dff.to_csv(os.path.join(pather))
    print('With Thread All took {} seconds'.format(tt.time() - starttime))

 # %%
