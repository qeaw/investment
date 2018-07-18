import os
import requests
import pandas as pd
import tushare as ts
from datetime import datetime

def chajing(s):
    return s[:2].upper() + "#" + s[2:]


gsb = ts.get_stock_basics()


def xuan(wenjianming,gsb):

    os.chdir(r"C:\stock_data")
    datadf = pd.read_table(wenjianming, skiprows=1, skipfooter=1, engine="python", parse_dates=True, )
    if len(datadf) < 50:
        return
    now_c = []
    for i in datadf.columns:
        i = i.strip(" ")
        now_c.append(i)
    datadf.columns = now_c

    qnow = datadf["成交额"][len(datadf) - 1]
    pnow = datadf["收盘"][len(datadf) - 1]
    rmin = datadf["成交额"].rolling(window=45).min()


    # rmax = datadf["成交额"].rolling(window=45).max()
    # rmean = datadf["成交额"].rolling(window=45).mean()

    dn = 0

    lj = 0



    zongliang = datadf["成交额"][len(datadf)-45:].sum()

    for i in range(45):
        qi = datadf["成交额"][len(datadf) - 1 - i]
        pi = datadf["收盘"][len(datadf) - 1 - i]
        pz = datadf["收盘"][len(datadf) - 2 - i]
        ri = (pi / pz) - 1
        dn += ((45 - i) / 45) * ri * qi
        lj += pi * qi

    dn = dn / zongliang
    lj = lj / zongliang
    shizhi = float(gsb.loc[wenjianming[3:-4]]["outstanding"]) * pnow #单位 亿
    # print(shizhi)




    if qnow!= 0 and qnow < rmin[len(datadf) - 2] and pnow < lj* 1.03 and pnow > lj * 0.97 and dn > 0.003 and shizhi< 200:
        gpdm = wenjianming[:2].lower() + wenjianming[3:-4]

        r = requests.get(f'http://hq.sinajs.cn/list={gpdm}')

        name = r.text.split(",")[0].split("=")[1].strip("\"")

        print(f"买入 {name}:{wenjianming[:-4]}, 量比{round(qnow /rmin[len(datadf) - 2],2)}，动能{round(dn,4)}，现价{pnow}, 加权价{round(lj,2)}")

        with open(r"C:\Users\qeaw\Desktop\rrr\result_xuangu\result.txt","a") as f:
            f.write(f"{datetime.now()} buy {name} {wenjianming[:-4]} at {pnow} \n")
        return True

    return False

n = 0
for i in os.listdir(r"C:\stock_data"):
    r = xuan(i,gsb)
    if r == True:
        n += 1

# xuan("SZ#002204.txt")

print(f"finish, find {n} stocks")




