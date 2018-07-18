import os, os.path
import requests
import tushare as ts
import pandas as pd

def chajing(s):
    return s + "moni" + ".txt"

def huifu(w):
    return w[:2] + w[3:9]

def huifushuzi(w):
    return w[3:9]

def mc(df,gpdm,i):
    pnows = df.loc[df.index[i]]["close"]
    print(f"卖出{gpdm} at {pnows} in day {df.index[i]}index{i}")
    name = r"C:\Users\qeaw\Desktop\test\monipan" + "\\" + chajing(gpdm)
    s = f"sell\t{gpdm}\t{df.index[i]}\t{pnows}\n"
    with open(name, "a") as f:
        f.write(s)

    return 0


def xianshi(gpdm):
    df = ts.get_hist_data(gpdm,"2016-03-02")
    if type(df) == type(None):
        return

    x = list(df.index)
    x.reverse()
    df = df.reindex(index = x)

    m1 = 0
    mm = 0
    # print(df.index)
    for i in range(45,len(df)-10):
        tp = df.loc[df.index[i]]["close"]
        yp = df.loc[df.index[i-1]]["close"]
        rate = tp / yp - 1

        if m1 > 0 :
            try:
                d = date_index
            except NameError:
                d = i
            if i > d:
                qmai = df.loc[df.index[i]]["volume"]
                x = sorted(df.loc[df.index[max(i - 90, 0)]:df.index[i - 1]]["volume"])
                qjunm = sum(x[len(x) - 3:]) / 3
                if qmai > qjunm:
                    m1 = mc(df, gpdm, i)
                    mm += 1

        if rate > 0.09:
            junq = df.loc[df.index[max(0,i-45)]:df.index[i-1]]["close"].mean()
            junh = df.loc[df.index[i+1]:df.index[min(i+30,len(df)-14)]]["close"].mean()
            if junh > junq:
                for j in range(i,len(df)-45):
                    qnow = df.loc[df.index[j]]["volume"]
                    pnow = df.loc[df.index[j]]["close"]
                    q_list = sorted(df.loc[df.index[max(j-90,0)]:df.index[j-1]]["volume"])
                    qjunx = sum(q_list[:3]) / 3
                    qjund = sum(q_list[len(q_list)-3:]) / 3


                    if qnow < qjunx and pnow > tp * 0.95 and pnow < tp * 1.05:
                        dongneng = 0
                        for k in range(max(0,j-90),j):
                            qq = sum(q_list) / len(q_list)
                            today_q = df.loc[df.index[k]]["volume"]
                            rate = df.loc[df.index[k]]["close"] / df.loc[df.index[k]]["open"] - 1
                            dongneng += (180 + k - j) / 180 * (rate * today_q / qq)
                        if dongneng > 0:
                            try:
                                ok = (j - ii) > 5
                            except NameError:
                                ok = True

                            if ok:
                                print(f"买入{gpdm} at {pnow} in day {df.index[j]} index{j}")
                                # print(df.loc[df.index[j]])
                                name = r"C:\Users\qeaw\Desktop\test\monipan" + "\\" + chajing(gpdm)
                                s = f"buy\t{gpdm}\t{df.index[j]}\t{pnow}\n"
                                with open(name, "a") as f:
                                    f.write(s)
                                m1 += 1
                                date_index = j
                                ii = j


                    if m1> 0 and qnow > qjund and i > j:
                        m1 = mc(df,gpdm,i)
                        mm += 1
    if m1 > 0 and mm == 0:
        pnow = df.loc[df.index[len(df)-1]]["close"]
        print(f"最后卖出{gpdm} at {pnow} in day {df.index[len(df)-1]} index{len(df)-1}")
        # print(df.index)
        name = r"C:\Users\qeaw\Desktop\test\monipan" + "\\" + chajing(gpdm)
        s = f"sell\t{gpdm}\t{df.index[len(df)-1]}\t{pnow}\n"
        with open(name, "a") as f:
            f.write(s)


def xianshi2(gpdm):
    df = ts.get_hist_data(gpdm,"2016-03-02")
    if type(df) == type(None):
        return
    # print(gpdm)
    # print(df)
    x = list(df.index)
    x.reverse()
    df = df.reindex(index = x)
    if len(df) < 200:
        return
    # print(df.loc[df.index[len(df)-1]])
    m1 = 0
    mm = 0
    # print(df.index)
    for i in range(len(df)-90,len(df)-10):
        tp = df.loc[df.index[i]]["close"]
        yp = df.loc[df.index[i-1]]["close"]
        rate = tp / yp - 1

        # if m1 > 0 :
        #     try:
        #         d = date_index
        #     except NameError:
        #         d = i
        #     if i > d:
        #         qmai = df.loc[df.index[i]]["volume"]
        #         x = sorted(df.loc[df.index[max(i - 90, 0)]:df.index[i - 1]]["volume"])
        #         qjunm = sum(x[len(x) - 3:]) / 3
        #         if qmai > qjunm:
        #             m1 = mc(df, gpdm, i)
        #             mm += 1

        if rate > 0.09:
            junq = df.loc[df.index[max(0,i-45)]:df.index[i-1]]["close"].mean()
            junh = df.loc[df.index[i+1]:df.index[min(i+30,len(df)-14)]]["close"].mean()
            if junh > junq:
                for j in range(len(df)-1,len(df)):
                    qnow = df.loc[df.index[len(df)-1]]["volume"]
                    pnow = df.loc[df.index[len(df)-1]]["close"]
                    q_list = sorted(df.loc[df.index[max(j-90,0)]:df.index[j-1]]["volume"])
                    qjunx = sum(q_list[:3]) / 3
                    qjund = sum(q_list[len(q_list)-3:]) / 3


                    if qnow < qjunx and pnow > tp * 0.95 and pnow < tp * 1.05:
                        dongneng = 0
                        for k in range(max(0,j-90),j):
                            qq = sum(q_list) / len(q_list)
                            today_q = df.loc[df.index[k]]["volume"]
                            rate = df.loc[df.index[k]]["close"] / df.loc[df.index[k]]["open"] - 1
                            dongneng += (180 + k - j) / 180 * (rate * today_q / qq)
                        if dongneng > 0:
                            try:
                                ok = (j - ii) > 5
                            except NameError:
                                ok = True

                            if ok:
                                print(f"买入{gpdm} at {pnow}")
                                # print(df.loc[df.index[j]])
                                # name = r"C:\Users\qeaw\Desktop\test\monipan" + "\\" + chajing(gpdm)
                                # s = f"buy\t{gpdm}\t{pnow}\n"
                                # with open(name, "a") as f:
                                #     f.write(s)
                                # m1 += 1
                                date_index = j
                                ii = j


                    # if m1> 0 and qnow > qjund and i > j:
                    #     m1 = mc(df,gpdm,i)
                    #     mm += 1
    # if m1 > 0 and mm == 0:
    #     pnow = df.loc[df.index[len(df)-1]]["close"]
    #     print(f"最后卖出{gpdm} at {pnow} in day {df.index[len(df)-1]} index{len(df)-1}")
    #     print(df.index)
        # name = r"C:\Users\qeaw\Desktop\test\monipan" + "\\" + chajing(gpdm)
        # s = f"sell\t{gpdm}\t{df.index[len(df)-1]}\t{pnow}\n"
        # with open(name, "a") as f:
        #     f.write(s)



os.chdir(r"C:\stock_data")
for i in os.listdir(r"C:\stock_data"):
    xianshi2(huifushuzi(i))
print("finish")





