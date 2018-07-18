import os

import pandas as pd


def chajing(s):
    return s[:2].upper() + "#" + s[2:]



def xianshi(gpdm):
    os.chdir(r"C:\stock_data")
    datadf = pd.read_table(gpdm, skiprows=1, skipfooter=1, engine="python", parse_dates=True, )
    now_c = []
    for i in datadf.columns:
        i = i.strip(" ")
        now_c.append(i)
    datadf.columns = now_c

    rmin = datadf["成交额"].rolling(window=30).min()
    rmax = datadf["成交额"].rolling(window=30).max()
    rmean = datadf["成交额"].rolling(window=30).mean()

    os.chdir(r"C:\Users\qeaw\Desktop\result")
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
    os.chdir(r"C:\Users\qeaw\Desktop\result2")
    with open(gpdm[:9] + "zongjie" + gpdm[9:], "a") as f:
        pingjun = pd.Series(result).mean()
        zong = pd.Series(result).product()
        print(f"平均收益：{pingjun}")
        print(f"总收益：{zong}")
        f.write(f"平均收益：{pingjun}\n")

        f.write(f"总收益：{zong}\n")

        f.write(f"正收益次数：{zheng}，负收益次数：{fu}\n")





def huice2(gpdm):
    os.chdir(r"C:\stock_data")
    datadf = pd.read_table(gpdm, skiprows=1, skipfooter=1, engine="python", parse_dates=True, )
    now_c = []
    for i in datadf.columns:
        i = i.strip(" ")
        now_c.append(i)
    datadf.columns = now_c
    rmin = datadf["成交额"].rolling(window=30).min()
    rmax = datadf["成交额"].rolling(window=30).max()
    os.chdir(r"C:\Users\qeaw\Desktop\new")
    with open(gpdm[:9] + "jieguo" + gpdm[9:], "a") as f:
        m = 0
        for i in range(30, len(datadf)):
            if datadf["成交额"][i] < rmin[i - 1] and i > m and not datadf.loc[i]["收盘"] > datadf.loc[i - 1][
                "收盘"] * 1.03 and not datadf.loc[i]["收盘"] < datadf.loc[i - 1]["收盘"] * 0.98:
                c = True
                n = i
                db = datadf.loc[i]["日期"]
                pb = datadf.loc[i]["收盘"]
                qb = datadf.loc[i]["成交额"]
                for j in range(n,len(datadf)):
                    if datadf["成交额"][j] > rmax[j-1] and c:
                        m = j
                        ds = datadf.loc[j]["日期"]
                        ps = datadf.loc[j]["收盘"]
                        qs = datadf.loc[j]["成交额"]
                        s =f"buy: {db}\t{pb}\t{qb}\nsell:{ds}\t{ps}\t{qs}\n"
                        f.write(s)
                        c = False














def huice_qb(gpdm):
    os.chdir(r"C:\stock_data")

    datadf = pd.read_table(gpdm, skiprows=1, skipfooter=1, engine="python", parse_dates=True, )

    now_c = []
    for i in datadf.columns:
        i = i.strip(" ")
        now_c.append(i)
    datadf.columns = now_c

    rmin = datadf["成交额"].rolling(window=30).min()
    rmax = datadf["成交额"].rolling(window=30).max()

    os.chdir(r"C:\Users\qeaw\Desktop\new\new2")

    with open(gpdm[:9] + "buy" + gpdm[9:], "a") as f:
        f.write("日期\t价格\t成交量\n")
        for i in range(30, len(datadf)):
            if datadf["成交额"][i] < rmin[i - 1]:
                # print(f"find buy point at:\n {datadf.loc[i]}")
                # mai3.append(datadf.loc[i].to_string())
                d = datadf.loc[i]["日期"]
                p = datadf.loc[i]["收盘"]
                q = datadf.loc[i]["成交额"]

                s = f"{d}\t{p}\t{q}\n"
                f.write(s)

    with open(gpdm[:9] + "sell" + gpdm[9:], "a") as f:
        f.write("日期\t价格\t成交量\n")
        for i in range(30, len(datadf)):
            if datadf["成交额"][i] > rmax[i - 1]:
                # print(f"find buy point at:\n {datadf.loc[i]}")
                # mai3.append(datadf.loc[i].to_string())
                d = datadf.loc[i]["日期"]
                p = datadf.loc[i]["收盘"]
                q = datadf.loc[i]["成交额"]

                s = f"{d}\t{p}\t{q}\n"
                f.write(s)








for i in os.listdir(r"C:\stock_data"):
    xianshi(i)


# g = "SH#600300.txt"
# xianshi(g)