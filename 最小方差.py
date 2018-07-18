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
    x = ts.get_k_data(gpdm, autype="qfq")
    if type(x) == type(None):
        return
    if len(x) < 150:
        return
    if x.date[len(x)-1] != "2018-07-17":
        return
    # pnow = x.close[len(x) - 1]
    # pmin = x.close[len(x) - 150:len(x) - 50].min()
    s2 = 0
    miu = sum([x.close[len(x) - i] for i in range(1,26)])/len([x.close[len(x) - i] for i in range(1,26)])
    for i in range(1,26):
        s2 += (x.close[len(x) - i] - miu)**2
    s2 /= 25
    sd = s2**0.5
    adsd = sd / miu
    print([adsd,gpdm])
    return [adsd,gpdm]


os.chdir(r"C:\Users\qeaw\Desktop\rrr\result2018-07-17")
ll = []
for i in os.listdir(r"C:\stock_data"):
    jieguo = xuangu(huifu(i))
    if type(jieguo) == list:
        ll.append(jieguo)

ll.sort()
print(ll)
with open("jieguo.txt","w") as f:
    f.write(str(ll))
