import tushare as ts
import os
from math import log
import numpy as np

def huifushuzi(w):
    return w[3:9]

def xuangu(gpdm):
    df = ts.get_hist_data(gpdm, "2016-03-02")
    if type(df) == type(None):
        return
    if len(df) < 300:
        return
    x = list(df.index)
    x.reverse()
    df = df.reindex(index=x)
    # first find buying siginal
    up = 0
    down = 0
    if df.close.min() * 2.5 < df.close.max():
        return
    if df.close[df.index[len(df)-50]:df.index[len(df)-20]].mean() > df.close[df.index[len(df)-20]:].mean():
        return
    zuidaliang = np.where(df.volume == max(df.volume[df.index[len(df)-45:]]))[0][0]
    # print(df.index[zuidaliang])
    if df.open[df.index[zuidaliang]] - df.close[df.index[zuidaliang]] > 0:
        # print(gpdm,"绿最大")
        return

    liang = []
    liangjia = 0
    hong = 0
    lv = 0
    for i in range(len(df)-45,len(df)):
        tp = df.loc[df.index[i]]["close"]
        yp = df.loc[df.index[i - 1]]["close"]
        rate = tp / yp - 1
        if df.open[df.index[i]] < df.close[df.index[i]]:
            hong += df.volume[i]
        if df.open[df.index[i]] > df.close[df.index[i]]:
                    lv += df.volume[i]

        if rate > 0.03:
            up += 1
            liang.append(df.volume[df.index[i]])

            liangjia += df.volume[df.index[i]] * df.close[df.index[i]]
        if rate < -0.05:
            down += 1
    if up >=3 and down < 1 and hong-lv>0:

        jiaquanjia = 0
        for j in range(0,len(df)-45):

            jiaquanjia += df.loc[df.index[j]]["close"] * df.loc[df.index[j]]["volume"]
        jiaquanjia /= df.volume.sum()

        if df.close[len(df)-1] < jiaquanjia:
            liangjia /= sum(liang)
            qjun = sum(liang) / len(liang)
            beta = (liangjia / df.close[df.index[len(df)-1]]) * log(qjun / df.volume[df.index[len(df)-1]],10)
            return ((beta,gpdm))




l = []
os.chdir(r"C:\stock_data")
for i in os.listdir(r"C:\stock_data"):
    x = xuangu(huifushuzi(i))
    if type(x) == tuple:
        l.append(x)
        l.sort(reverse=True)
        print(l)
# gpdm = "600232"
# xuangu(gpdm)



