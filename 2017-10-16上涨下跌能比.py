import tushare as ts
import os
import requests
from math import log

def huifushuzi(w):
    return w[3:9]


gpdm = "002304"

def fenxi(gpdm):
    df = ts.get_k_data(gpdm, "2017-05-15",autype="qfq")
    if type(df) == type(None):
        return
    if len(df) < 90:
        print(f"{gpdm}buzu")
        return
    if df.close.min() * 2 < df.close.max():
        return
    if df.close[len(df)-1] > df.close.mean():
        return


    pnow = df.close[df.index[len(df) - 1]]
    qnow = df.volume[df.index[len(df) - 1]]
    qjun = df.volume.mean()
    lmdu = 0
    lmdd = 0
    # l1 = False
    # l2 = False

    for i in range(1,len(df)):

        tp = df.loc[df.index[i]]["close"]
        tq = df.loc[df.index[i]]["volume"]
        yp = df.loc[df.index[i - 1]]["close"]
        rate = tp / yp - 1
        # print(df.index[i], rate, pnow,tp)
        if tp > pnow and rate > 0:
            lmdu += ((i+100)/200) * (tp / pnow) * max(log(tq/qnow,10),1) * rate
            # print(f"date: {df.date[df.index[i]]} 当前：{pnow} 当日：{tp} up zengliang:{((i+100)/200) * (tp / pnow) * max(log(tq/qnow,10),1) * rate}")
            # l1 = True

        if tp < pnow and rate < 0:
                lmdd += ((i+100)/200) * (pnow / tp) * max(log(tq/qnow,10),1) * abs(rate)
                # l2 = False
                # print(f"date: {df.date[df.index[i]]} down zengliang:{((i+100)/200) * (pnow / tp) * max(log(tq/qnow,10),1) * abs(rate)}")
    # if l1 == False:
    #     lmdu = -999
    # if l2 == False:
    #     lmdd = 999


    # with open(r"C:\Users\qeaw\Desktop\test\lambda\result.txt","a") as f:
    #     f.write(f"{gpdm}\t{lmdu}\t{lmdd}\n")
    print(f"{gpdm}\t{lmdu}\t{lmdd}")

# for i in os.listdir(r"C:\stock_data"):
#     fenxi(huifushuzi(i))

fenxi(gpdm)




