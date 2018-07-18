import tushare as ts
import os
from time import sleep
import urllib
from datetime import datetime
import sys
def daxie(number):
    num = int(number)
    num_str = str(num)
    leng = len(num_str)
    wei = ["元", "十", "百", "千", "万", "十万", "百万", "千万", "亿", "十亿", "百亿"]
    result = num_str[0] + wei[len(num_str) - 1] + num_str[1] + wei[len(num_str) - 2]
    return result

def huifushuzi(w):
    return w[3:9]

rq = str(input("输入前一天的日期："))

def fenxi(gpdm,rq):


    # qsrq = "2017-01-10"
    # jsrq = "2017-10-18"


    x = ts.get_k_data(gpdm,start = rq)
    y = ts.get_k_data(gpdm)

    if len(y) < 50:
        return

    zc = float(x.loc[x.index[0]].close)
    jc = float(x.loc[x.index[1]].close)
    jl = float(x.loc[x.index[1]].low)

    rate=  jc / zc - 1
    ratel = jl / zc - 1

    return [rate,ratel,gpdm]

# print(fenxi("002594",rq))

ll = []

for i in os.listdir(r"C:\stock_data"):
    print(huifushuzi(i),rq)
    try:
        jieguo = fenxi(huifushuzi(i),rq)
        if type(jieguo) == list:
            ll.append(jieguo)
            ll.sort(key= lambda s: s[0] + s[1], reverse= True)
            print(ll[:10],len(ll))
    except:
        pass
#     sleep(1)
#
os.chdir(r"C:\Users\qeaw\Desktop\rrr\2017-11-07")
with open("jieguo.txt","w") as f:
    f.write(str(ll))
#

