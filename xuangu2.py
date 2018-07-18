import os
import requests
import pandas as pd
import tushare as ts
from datetime import datetime

def chajing(s):
    return s[:2].upper() + "#" + s[2:]

def huifu(w):
    return w[:2] + w[3:9]


# gsb = ts.get_stock_basics()


def xuan(wenjianming):


    datadf = pd.read_table(wenjianming, skiprows=1, skipfooter=1, engine="python", parse_dates=True, )
    if len(datadf) < 250:
        return
    now_c = []
    for i in datadf.columns:
        i = i.strip(" ")
        now_c.append(i)
    datadf.columns = now_c


    # r90 = datadf["成交额"].rolling(window=90).min()
    # r35 = datadf.loc[len(datadf)-10:]["成交额"].rolling(window=45).min()
    # r10 = datadf["成交额"].rolling(window=10).min()
    for i in range(len(datadf)-45,len(datadf)-10):
        pdangtian = datadf["收盘"][i]
        pzuo = datadf["收盘"][i-1]
        rate = (pdangtian / pzuo) - 1
        # print(rate)
        if rate > 0.11:
            # print("not stock")
            return False
        # print(rate)
        if rate > 0.09:

            # print(rate,wenjianming,datadf["日期"][i])
            pjunh = datadf["收盘"][i:].mean()
            pjunq = datadf["收盘"][i-30:i].mean()
            pzhangting = datadf["收盘"][i]
            if pjunh > pjunq:
                qnow = datadf["成交额"][len(datadf) - 1]
                pnow = datadf["收盘"][len(datadf) - 1]

                qjun = datadf["成交额"][len(datadf) - 91:len(datadf) - 2].tolist()
                qjun.sort()
                qjun = sum(qjun[:3]) / 3
                if qnow <= qjun and pnow < pzhangting * 1.05 and pnow > pzhangting * 0.95:
                    print(huifu(wenjianming),pnow,pzhangting,datadf["日期"][len(datadf) - 1])
                    return True
    # print("no")


os.chdir(r"C:\stock_data")
n = 0
for i in os.listdir(r"C:\stock_data"):
    r = xuan(i)
    if r == True:
        n += 1
        print(n)
