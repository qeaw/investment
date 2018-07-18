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
    x = ts.get_k_data(gpdm,autype="hfq")
    if type(x) == type(None):
        return
    if len(x) < 150:
        return

    for i in range(len(x)-60,len(x) - 1):
        ratec = x.close[i] / x.close[i-1] - 1
        if ratec > 0.095:
            kai = x.open[i]
            di = x.low[i]
            zuo = x.close[i-1]
            liangd = x.volume[i]
            liangz = x.volume[i-1]
            now = datetime.now()
            ddd = datetime.strptime(x.date[x.index[len(x) - 1]], "%Y-%m-%d")


            if kai / zuo -1 > 0.08 and di / zuo - 1 > 0.06 and di / zuo - 1< 0.09 and liangd > liangz * 3 and (now - ddd).days < 5:
                link = r"http://image.sinajs.cn/newchart/daily/n/" + gpdm + ".gif"
                y = requests.get(link)
                name = gpdm + ".jpg"
                with open(name,"wb") as f:
                    f.write(y.content)
                print(f"found{gpdm}")
                return gpdm




os.chdir(r"C:\Users\qeaw\Desktop\rrr\result2017-10-27")
ll = []
for i in os.listdir(r"C:\stock_data"):
    jieguo = fenxi(huifu(i))
    if type(jieguo) == str:
        ll.append(jieguo)


print(ll)
with open("jieguo.txt","w") as f:
    f.write(str(ll))