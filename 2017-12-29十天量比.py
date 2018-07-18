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

def xuangu(gpdm):
    x = ts.get_k_data(gpdm, autype="qfq")
    if type(x) == type(None):
        return
    if len(x) < 150:
        return
    pnow = x.close[len(x)-1]
    pmin = x.close[len(x)-150:len(x)-50].min()

    if pnow < pmin * 1.1:
        if (x.close[len(x)-15:].max() - x.close[len(x)-15:].min()) / x.close[len(x)-15:].min() < 0.05:
            zl = 0
            dl = 0
            for i in range(len(x) - 20, len(x) - 1):
                tp = x.loc[x.index[i]]["close"]
                yp = x.loc[x.index[i - 1]]["close"]
                rate = tp / yp - 1
                if rate > 0:
                    zl += x.loc[x.index[i]]["volume"]
                if rate < 0:
                    dl += x.loc[x.index[i]]["volume"]
            if zl > dl * 1.5:
                r = x.loc[len(x) - 150:len(x) - 50].rolling(window=10)
                vvmin = r.sum().volume.min()
                vvnow = x.volume[len(x) - 10:].sum()
                if vvnow < vvmin:
                    for i in range(len(x)-50, len(x)-1):
                        tp = x.loc[x.index[i]]["close"]
                        yp = x.loc[x.index[i - 1]]["close"]

                        rate = tp / yp - 1
                        print(rate)
                        if rate < -0.095:
                            print(f"{gpdm}dietingquchu")
                            return

                    link = r"http://image.sinajs.cn/newchart/daily/n/" + gpdm + ".gif"
                    y = requests.get(link)
                    name = gpdm + ".jpg"
                    # os.chdir(r"C:\Users\qeaw\Desktop\rrr\result2017-12-22")
                    with open(name, "wb") as f:
                        f.write(y.content)
                    print(f"found{gpdm}")
                    return gpdm


# os.chdir(r"C:\Users\qeaw\Desktop\rrr\result2017-12-31")
# ll = []
# for i in os.listdir(r"C:\stock_data"):
#     jieguo = xuangu(huifu(i))
#     if type(jieguo) == str:
#         ll.append(jieguo)
#
#
# print(ll)
# with open("jieguo.txt","w") as f:
#     f.write(str(ll))

print(xuangu("002719"))