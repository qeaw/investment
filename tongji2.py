import pandas as pd

import os

def huifu(s):
    return s[:9] + s[16:]

f = open(r"C:\Users\qeaw\Desktop\tongji\fude.txt","r")

s = f.read()

f.close()

l = eval(s[4:])
ll = [huifu(i) for i in l]

os.chdir(r"C:\stock_data")

def xianshi(gpdm):
    os.chdir(r"C:\stock_data")
    df = pd.read_table(gpdm, skiprows=1, skipfooter=1, engine="python", parse_dates=True, )

    now_c = []
    for i in df.columns:
        i = i.strip(" ")
        now_c.append(i)
    df.columns = now_c

    datadf = df.loc[1028:]
    datadf.index = range(len(datadf))

    rmin = datadf["成交额"].rolling(window=30).min()
    rmax = datadf["成交额"].rolling(window=30).max()
    rmean = datadf["成交额"].rolling(window=30).mean()

    os.chdir(r"C:\Users\qeaw\Desktop\rrr\result3")
    result = []
    m = 0
    for i in range(30, len(datadf)):
        dn = 0
        liangjia = 0
        liang = 0
        for j in range(1, 30):
            pricen = datadf.loc[i - j]["收盘"]
            pricey = datadf.loc[i - j - 1]["收盘"]
            rate = (pricen / pricey) - 1
            v = datadf.loc[i - j]["成交额"]
            vv = v / rmean[i - j]
            zhongjian =((30-j) / 30)*  rate * vv
            liangjia += pricen * v
            liang += v
            dn += zhongjian


        if datadf["成交额"][i] < rmin[i - 1] and datadf["收盘"][i] <= liangjia / liang and dn > 0 and i > m and not datadf.loc[i]["收盘"] > datadf.loc[i - 1][
            "收盘"] * 1.03 and not datadf.loc[i]["收盘"] < datadf.loc[i - 1]["收盘"] * 0.98:
            c = True
            n = i
            db = datadf.loc[i]["日期"]
            pb = datadf.loc[i]["收盘"]
            qb = datadf.loc[i]["成交额"]
            print(db,dn)
            for j in range(n, len(datadf)):
                if datadf["成交额"][j] > rmax[j - 1] and c:
                    m = j
                    ds = datadf.loc[j]["日期"]
                    ps = datadf.loc[j]["收盘"]
                    qs = datadf.loc[j]["成交额"]

                    s = ps / pb
                    result.append(s)
                    ss = f"buy: {db}\t{pb}\t{qb}\nsell:{ds}\t{ps}\t{qs}\n"
                    with open(gpdm[:9] + "jiaoyi" + gpdm[9:], "a") as f:
                        f.write(ss)

                    c = False

    zheng =0
    fu = 0
    for i in result:
        if i>1:
            zheng +=1
        if i<1:
            fu += 1
    os.chdir(r"C:\Users\qeaw\Desktop\rrr\result4")
    with open(gpdm[:9] + "zongjie" + gpdm[9:], "a") as f:
        pingjun = pd.Series(result).mean()
        zong = pd.Series(result).product()
        print(f"平均收益：{pingjun}")
        print(f"总收益：{zong}")
        f.write(f"平均收益：{pingjun}\n")

        f.write(f"总收益：{zong}\n")

        f.write(f"正收益次数：{zheng}，负收益次数：{fu}\n")



for i in ll:
    xianshi(i)