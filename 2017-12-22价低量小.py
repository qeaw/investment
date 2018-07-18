import tushare as ts
import requests
import os
from datetime import datetime
def chajing(s):
    return s[:2].upper() + "#" + s[2:]

def huifushuzi(w):
    return w[3:9]

def huifu(w):
    return w[0:2].lower() + w[3:9]

def fenxi(gpdm):
    x = ts.get_k_data(gpdm,autype="qfq")
    if type(x) == type(None):
        return
    if len(x) < 150:
        return

    todayp = x.loc[len(x)-1].close
    todayq = x.loc[len(x)-1].volume

    minp = x.loc[len(x)- 120:len(x)- 50].close.min()
    minq = x.loc[len(x)- 120:len(x)- 50].volume.min()

    if todayp < minp * 1.1 and  todayp > minp * 0.9 and todayq < minq * 1.2:
        qzhang = 0
        qdie = 0
        for i in range(len(x) - 20, len(x) - 1):
            ratec = x.close[i] / x.close[i - 1] - 1
            if ratec > 0.008:
                qzhang += x.volume[i]
            if ratec < -0.008:
                qdie += x.volume[i]
        if qzhang > qdie * 2:
            link = r"http://image.sinajs.cn/newchart/daily/n/" + gpdm + ".gif"
            y = requests.get(link)
            name = gpdm + ".jpg"
            # os.chdir(r"C:\Users\qeaw\Desktop\rrr\result2017-12-22")
            with open(name, "wb") as f:
                f.write(y.content)
            print(f"found{gpdm}")
            return gpdm







os.chdir(r"C:\Users\qeaw\Desktop\rrr\result2017-12-28")
ll = []
for i in os.listdir(r"C:\stock_data"):
    jieguo = fenxi(huifu(i))
    if type(jieguo) == str:
        ll.append(jieguo)


print(ll)
with open("jieguo.txt","w") as f:
    f.write(str(ll))



