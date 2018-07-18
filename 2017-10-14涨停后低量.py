import os
import tushare as ts
from math import log
from datetime import datetime

def huifushuzi(w):
    return w[3:9]

def xuangu(gpdm):
    df = ts.get_k_data(gpdm, "2016-03-02",autype="qfq")
    if type(df) == type(None):
        return
    if len(df) < 301:
        return
    now = datetime.now()
    x = datetime.strptime(df.date[df.index[len(df)-1]],"%Y-%m-%d")
    if (now-x).days > 10:
        return

    you = 0
    di =0
    if df.volume[df.index[len(df)-1]] == 0:
        return
    for i in range(len(df)-50,len(df)-10):
        tp = df.loc[df.index[i]]["close"]
        yp = df.loc[df.index[i - 1]]["close"]
        rate = tp / yp - 1
        if rate > 0.09:
            you += 1
            date = i
            qs = df.volume[df.index[i]]
            break
    if you > 0:
        liangjia = 0
        for j in range(len(df)-300,len(df)-50):
            liangjia += df.loc[df.index[j]]["close"] * df.loc[df.index[j]]["volume"]
        liangjia /= df.volume.sum()
        if df.close[len(df)-1] <= liangjia:
            di += 1
    if di > 0:
        if df.close[df.index[len(df)-300]:df.index[len(df)-50]].max() / df.close[df.index[len(df)-300]:df.index[len(df)-50]].min() < 2.5:
            # print(gpdm)
            liangjia2 = 0
            pq = 0
            nq = 0
            for k in range(date,len(df)-1):
                liangjia2 += df.loc[df.index[j]]["close"] * df.loc[df.index[j]]["volume"]
                if df.close[df.index[k]] > df.open[df.index[k]] * 1.01:
                    pq += df.volume[df.index[k]]
                if df.close[df.index[k]] < df.open[df.index[k]] * 0.99:
                    nq += df.volume[df.index[k]]

            liangjia2 /= df.volume.sum()
            beta = liangjia2 / df.close[df.index[len(df)-1]] * log(qs/df.volume[df.index[len(df)-1]],10) * log(pq/nq,10)




            # print(beta)
            return((beta,gpdm))




os.chdir(r"C:\stock_data")
result = []
for i in os.listdir(r"C:\stock_data"):
    x = xuangu(huifushuzi(i))
    if type(x) == tuple:
        result.append(x)
    result.sort()
    print(result)



print(result)
