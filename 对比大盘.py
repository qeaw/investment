import os, glob
import pandas as pd
import numpy as np
import requests
from datetime import timedelta

def chajing(s):
    return s[:2].upper() + "#" + s[2:]

def huifu(w):
    return w[:2] + w[3:9]



def comp(wenjianming):

    datadf = pd.read_table(wenjianming, skiprows=1, skipfooter=1, engine="python", parse_dates=True, index_col = 0)
    if len(datadf) < 250:
        return
    dapan = pd.read_table("SH#999999.txt", skiprows=1, skipfooter=1, engine="python", parse_dates=True, index_col = 0)
    now_c = []
    for i in datadf.columns:
        i = i.strip(" ")
        now_c.append(i)
    datadf.columns = now_c
    dapan.columns = now_c
    datadf = datadf.reindex(index=dapan.index)
    tianshu = 90
    dapan = dapan[len(dapan) - tianshu:]
    datadf = datadf[len(datadf) - tianshu:]


    start = datadf.index[0]
    jieguo = 0
    # print(dapan)
    # print(datadf.index)
    # print(datadf.index)
    # print(dapan.index)
    for i in dapan.index[1:]:
        pricei = datadf.loc[i]["收盘"]
        try:
            pricej = datadf.loc[i - timedelta(days=1)]["收盘"]
        except KeyError:
            try:
                pricej = datadf.loc[i - timedelta(days=3)]["收盘"]
            except:
                continue
        rate = (pricei / pricej) - 1

        if rate > -1:
            di = dapan.loc[i]["收盘"]

            try:
                dj = dapan.loc[i - timedelta(days=1)]["收盘"]
            except KeyError:
                try:
                    dj = dapan.loc[i - timedelta(days=3)]["收盘"]
                except KeyError:
                    continue

            try:
                dr = (di / dj) - 1
            except UnboundLocalError:
                dr = 0
            if jieguo == 0:
                pass
            jieguo += rate / dr

    (jieguo, huifu(wenjianming))
    return (jieguo,huifu(wenjianming))



os.chdir(r"C:\stock_data")
# w = 'SH#600020.txt'
# print(comp(w))
ll = []
for i in glob.glob("SH*.txt"):
    x = comp(i)
    if type(x) == tuple:
        ll.append(x)
#
ll.sort()
print(ll)