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
    r = ts.get_k_data(gpdm,"2010-1-1")
    if type(r) == type(None):
        return
    if len(r) < 500:
        return
    l = []
    # print(r.index,len(r))
    # return
    for i in range(r.index[0],len(r) + r.index[0],250):
        l.append(i)
    if l[-1] < r.index[len(r)-1]-100:
        l.append(r.index[len(r)-1])
    # print(l)
    # print(r.index,len(r))

    p_l = []

    for i in range(len(l)-1):
        data = r.loc[l[i]:l[i+1]]
        # print(data)
        zong = (data.close * data.volume).sum()
        vo = data.volume.sum()
        p = zong / vo

        p_l.append(p)
        # print(r.date[l[i]],r.date[l[i+1]],p)
    if len(p_l) < 2:
        return

    rate = (p_l[-1] / p_l[0]) / (len(l)-1)
    if type(rate) != numpy.float64:
        return

    return [rate,p_l,gpdm]

# gpdm = "600604"
#
# print(xuangu(gpdm))


os.chdir(r"C:\Users\qeaw\Desktop\rrr\result2018-01-07")
ll = []
for i in os.listdir(r"C:\stock_data"):
    jieguo = xuangu(huifu(i))
    print(jieguo)
    if type(jieguo) == list:
        ll.append(jieguo)



ll.sort()
print(ll[:10])
print(ll[len(ll)-10:])
with open("jieguo.txt","w") as f:
    f.write(str(ll))