import pandas as pd
import os

import requests

def chajing(s):
    return s[:2].upper() + "#" + s[2:]

def wst(gpdm,):
    os.chdir("C:\stock_data")
    datadf = pd.read_table(chajing(gpdm) + ".txt", skiprows=2, skipfooter=1, header=None, engine='python',
                           parse_dates=False)

    start_index = len(datadf[0]) - 27
    end_index = len(datadf[0]) - 1
    rishu = start_index - end_index

    print(type(datadf[start_index:][4]))
    cheng = 0
    liang = 0
    for i in range(start_index, len(datadf)):
        cheng += datadf.ix[i][4] * datadf.ix[i][5]
        liang += datadf.ix[i][5]
    print(cheng / liang)


wst("sz002268")

def sbqx(gpdm):
    os.chdir("C:\stock_data")
    datadf = pd.read_table(chajing(gpdm) + ".txt", skiprows=2, skipfooter=1, header=None, engine='python',
                           parse_dates=False)

    start_index = len(datadf[0]) - 39


    print(type(datadf[start_index:][4]))
    cheng = 0
    liang = 0
    for i in range(start_index, len(datadf)):
        cheng += datadf.ix[i][4] * datadf.ix[i][5]
        liang += datadf.ix[i][5]
    print(cheng / liang)

sbqx("sh600604")