import os
import pandas as pd
import requests
import tushare as ts


def chajing(s):
    return s[:2].upper() + "#" + s[2:]

def huifu(w):
    return w[:2] + w[3:9]



def xianshi(wenjianming):
    os.chdir(r"C:\stock_data")
    datadf = pd.read_table(wenjianming, skiprows=1, skipfooter=1, engine="python", parse_dates=True, )
    if len(datadf) < 250:
        return
    now_c = []
    for i in datadf.columns:
        i = i.strip(" ")
        now_c.append(i)
    datadf.columns = now_c

    df = datadf.loc[len(datadf)-200:]
    l_q = []
    l_r = []
    for i in range(1,len(df)):
        pricei = datadf.loc[i]["收盘"]
        pricej = datadf.loc[i - 1]["收盘"]
        rate = (pricei / pricej) - 1
        if rate > 0.03:
            qi = datadf.loc[i]["成交额"]
            l_r.append(rate)
            l_q.append(qi)
    if len(l_q) == 0:
        return
    qj = sum(l_q) / len(l_q)
    l_q = [i / qj for i in l_q]

    result = pd.Series([i/j for i in l_q for j in l_r])
    rz = result.diff()
    n = len(rz)
    zheng = 0
    for i in rz:
        if i > 0:
            zheng += 1
    if zheng == 0:
        return
    r = zheng / n

    return (r,huifu(wenjianming))







# w = [r"SH#600020.txt",r"SH#600018.txt",r"SH#600011.txt"]
ll = []
for i in os.listdir(r"C:\stock_data"):
    x = xianshi(i)
    if type(x) == tuple:
        ll.append(x)
        # print(ll)


ll.sort()
print(ll)

