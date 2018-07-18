import tushare as ts
import requests
import os
from datetime import datetime
import numpy
def chajing(s):
    return s[:2].upper() + "#" + s[2:]

def huifushuzi(w):
    return w[3:9]

def huifu(w):
    return w[0:2].lower() + w[3:9]

def xuangu(gpdm):
    r = ts.get_k_data(gpdm, "2017-05-01")
    if type(r) == type(None):
        return
    if len(r) < 140:
        return
    junliang = r.volume.sort_values()[:10].mean()
    if r.volume[r.index[0] + len(r) - 1] < junliang :
        # print(r.volume.sort_values())
        # print(gpdm, str(junliang))
        pn = r.close[r.index[0] + len(r) - 1]
        zheng = 0
        fu = 0
        for i in range(1,len(r)):
            if r.open[r.index[0] + i] < pn:
                rate = (r.close[r.index[0] + i - 1] - r.open[r.index[0] + i - 1]) / r.open[r.index[0] + i - 1]
                if rate > 0:
                    zheng += 1
                if rate < 0:
                    fu += 1
        if fu == 0:
            fu = 1
        return (zheng / fu, gpdm)

os.chdir(r"C:\Users\qeaw\Desktop\rrr\result2018-01-18")
ll = []
# gpdm = "600167"
# xuangu(gpdm)


for i in os.listdir(r"C:\stock_data"):
    jieguo = xuangu(huifu(i))
    print(jieguo)
    if type(jieguo) == tuple:
        ll.append(jieguo)


ll.sort()
print(ll[:10])
print(ll[len(ll)-10:])
with open("jieguo.txt","w") as f:
    f.write(str(ll))
