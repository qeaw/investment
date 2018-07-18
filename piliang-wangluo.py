import tkinter,time
import requests
import os
# from tkinter import Tk,Button,mainloop
import numpy as np
import pandas as pd
import smtplib
from email.mime.text import MIMEText
import tushare as ts

from pandas import DataFrame, Series
from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta
import itchat
import tushare as ts
itchat.auto_login(hotReload=False)



stock_l = ["sh600526","sh603017","sz002795","sz002824",
           "sz300008","sh600892","sz300052","sh600380",
           "sz002642","sz002166","sz002735","sh603177",
           "sh603011","sh601811","sh601016","sh600391",
           "sh600386","sh600070","sh600238","sz300348",
           "sz002329","sh600872","sh600386"]


def chajing(s):
    return s[:2].upper() + "#" + s[2:]


def huifu(w):
    return w[:2] + w[3:9]
def huifushuzi(w):
    return w[3:9]


def daxie(number):
    num = int(number)
    num_str = str(num)
    leng = len(num_str)
    wei = ["元", "十", "百", "千", "万", "十万", "百万", "千万", "亿", "十亿", "百亿"]
    result = num_str[0] + wei[len(num_str) - 1] + num_str[1] + wei[len(num_str) - 2]
    return result

def print_daxie(s,number,daima,n,p,rate):
    num = int(number)
    num_str = str(num)
    leng = len(num_str)
    wei = ["元", "十", "百", "千", "万", "十万", "百万", "千万", "亿", "十亿", "百亿"]
    result = num_str[0] + wei[len(num_str) - 1]
    print(s, daima, n, result,p,rate)

def send_email(user, pwd, dest, sub, text):
    msg = MIMEText(text)
    msg["Subject"] = sub
    msg["From"] = user
    msg["To"] = dest
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    s.login(user, pwd)
    s.sendmail(user, dest, msg.as_string())
    s.quit()
    print("finish")
    # pass

def show(content):
    # messagebox.showinfo(title = 'quantity remaind', message = content)
    pass

_user = "2458742185@qq.com"
_pwd = "mjraaenynfaadjfi"
_to = "407129740@qq.com"

def jiance(gpdm):

    if datetime.now().hour < 9:
        print(f"sleep{(datetime.now().replace(hour=9,minute=25) - datetime.now()).seconds}seconds,{(datetime.now().replace(hour=9,minute=25) - datetime.now()).seconds / 60} minutes")
        time.sleep((datetime.now().replace(hour=9,minute=25) - datetime.now()).seconds)
    if datetime.now().hour > 11 and datetime.now().hour < 13:
        print(f"sleep{(datetime.now().replace(hour=13,minute=0) - datetime.now()).seconds}seconds,{(datetime.now().replace(hour=13,minute=0) - datetime.now()).seconds / 60} minutes")
        time.sleep((datetime.now().replace(hour=13,minute=0) - datetime.now()).seconds)


    gpdms = gpdm[2:]
    wenjianming = gpdms


    datadf = ts.get_k_data(gpdms,autype="qfq")

    if type(datadf) == type(None):
        print(gpdm,"NoneType")
        return
    if len(datadf) < 100:
        print(gpdm,"duan")
        return


    now = datetime.now()
    x = datetime.strptime(datadf.date[datadf.index[0] +len(datadf) - 1], "%Y-%m-%d")
    # print(gpdm,datadf.index[0])
    if (now - x).days > 15:
        print(gpdm,"tingpan")
        return

    qnow = datadf.volume[datadf.index[datadf.index[0] + len(datadf) - 1]]
    pnow = datadf.close[datadf.index[datadf.index[0] + len(datadf) - 1]]
    minmean = datadf.volume[datadf.index[datadf.index[0] + len(datadf) - 45]:datadf.index[datadf.index[0] + len(datadf) - 1]].min()
    maxmean = sum(sorted(datadf.volume[datadf.index[datadf.index[0] + len(datadf) - 45]:datadf.index[datadf.index[0] + len(datadf) - 1]])[42:]) / 3








    print(f"开始监测{gpdm}", minmean, maxmean, round(minmean / maxmean, 2))

    dn = 0

    lj = 0

    zongliang = datadf.volume[datadf.index[datadf.index[0] + len(datadf) - 45]:].sum()

    for i in range(45):
        qi = datadf.volume[datadf.index[datadf.index[0] + len(datadf) - 1 - i]]
        pi = datadf.close[datadf.index[datadf.index[0] + len(datadf) - 1 - i]]
        pz = datadf.close[datadf.index[datadf.index[0] + len(datadf) - 2 - i]]

        ri = (pi / pz) - 1
        dn += ((45 - i) / 45) * ri * qi
        lj += pi * qi

    dn = dn / zongliang
    lj = lj / zongliang




    result = []
    n = 0
    while True:
        now = datetime.now()
        r = requests.get(f'http://hq.sinajs.cn/list={gpdm}')
        k = float(r.text.split(',')[1])
        s = float(r.text.split(',')[2])

        v = int(float(r.text.split(',')[8])) / 100
        p = float(r.text.split(',')[3])
        name = r.text.split(",")[0].split("=")[1].strip("\"")
        rate = str(round((p / s - 1) * 100, 3)) + "%"



        print_daxie(datetime.now(), v, gpdm, name, p, rate)
        # send_email(_user,_pwd,_to,"volume remaind", f"current volume{q}")
        if now.hour == 10 and now.minute == 30:
            predq = v * 4
            if predq > maxmean:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}, 量比{round(v / minmean,2)}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}, 量比{round(v / minmean,2)}")
                show(f"sell for predicted quantity is high at {predq}")
                result.append([v, p, now, "sell"])
            if predq < minmean and qnow!= 0 and p < lj* 1.03 and p > lj * 0.97 and dn > 0:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{huifu(wenjianming)}: 现成交量 {daxie(v)}，现价{p}，涨幅{rate},量比{round(v / maxmean,2)}")
                # itchat.search_friends(name="禅语")[0].send(f"买入 {name}{gpdm}: 现成交量 {daxie(q)}，现价{p}，涨幅{rate},量比{round(q / maxmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{huifu(wenjianming)}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}, 量比{round(v / maxmean,2)}")
                show(f"buy for predicted quantity is low at {predq}")
                result.append([v, p, now, "buy"])
        if now.hour == 11 and now.minute == 25:
            predq = v * 2
            if predq > maxmean:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{wenjianming}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}, 量比{round(v / minmean,2)}")
                show(f"sell for predicted quantity is high at {predq}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{huifu(wenjianming)}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}, 量比{round(v / minmean,2)}")
                result.append([v, p, now, "sell"])

            if predq < minmean and qnow!= 0 and p < lj* 1.03 and p > lj * 0.97 and dn > 0:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{wenjianming}: 现成交量 {daxie(v)}，现价{p}，涨幅{rate},量比{round(v / maxmean,2)}")
                # itchat.search_friends(name="禅语")[0].send(f"买入 {name}{gpdm}: 现成交量 {daxie(q)}，现价{p}，涨幅{rate},量比{round(q / maxmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{huifu(wenjianming)}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}, 量比{round(v / maxmean,2)}")
                show(f"buy for predicted quantity is low at {predq}")
                result.append([v, p, now, "buy"])
        if now.hour == 14 and now.minute == 0:
            predq = v * 4 / 3
            if predq > maxmean:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{wenjianming}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}, 量比{round(v / minmean,2)}")
                show(f"sell for predicted quantity is high at {predq}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{huifu(wenjianming)}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}, 量比{round(v / minmean,2)}")
                result.append([v, p, now, "sell"])
            if predq < minmean and qnow!= 0 and p < lj* 1.03 and p > lj * 0.97 and dn > 0:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{wenjianming}: 现成交量 {daxie(v)}，现价{p}，涨幅{rate},量比{round(v / maxmean,2)}")
                # itchat.search_friends(name="禅语")[0].send(f"买入 {name}{gpdm}: 现成交量 {daxie(q)}，现价{p}，涨幅{rate},量比{round(q / maxmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{huifu(wenjianming)}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}, 量比{round(v / maxmean,2)}")
                show(f"buy for predicted quantity is low at {predq}")

                result.append([v, p, now, "buy"])
        if now.hour == 14 and now.minute == 50:
            predq = v
            if predq > maxmean:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{wenjianming}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}, 量比{round(v / minmean,2)}")
                show(f"sell for predicted quantity is high at {predq}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{huifu(wenjianming)}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}, 量比{round(v / minmean,2)}")
                result.append([v, p, now, "sell"])
            if predq < minmean and qnow != 0 and p < lj*1.03 and p > lj*0.97 and dn > 0:
                send_email(_user, _pwd, _to, "交易提醒",
                           f"买入 {name}{wenjianming}: 现成交量 {daxie(v)}，现价{p}，涨幅{rate},量比{round(v / maxmean,2)}")
                # itchat.search_friends(name="禅语")[0].send(f"买入 {name}{gpdm}: 现成交量 {daxie(q)}，现价{p}，涨幅{rate},量比{round(q / maxmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{huifu(wenjianming)}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}, 量比{round(v / maxmean,2)}")
                show(f"buy for predicted quantity is low at {predq}")
                result.append([v, p, now, "buy"])

        if v > maxmean and n < 1:
            send_email(_user, _pwd, _to, "成交量提醒",
                       f"现在卖出 {name}{wenjianming}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}, 量比{round(v / minmean,2)}")
            show(f"sell for predicted quantity is high at {v}")
            # itchat.search_friends(name="禅语")[0].send(f"现在卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
            itchat.search_chatrooms(name="triple_group")[0].send(
                f"现在卖出 {name}{huifu(wenjianming)}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}, 量比{round(v / minmean,2)}(之后不再提醒)")
            result.append([v, p, now, "sell"])
            n += 1
            # time.sleep(1800)
        # if q < minmean:
        #     send_email(_user, _pwd, _to, "volume remaind", f"buy:current volume {q}")
        #     show(f"buy for predicted quantity is low at {q}")
        #     result.append([q, p, now,"buy"])
        time.sleep(59)
        if now.hour >= 15:
            os.chdir(r'C:\Users\qeaw\Desktop\test')
            with open(gpdm +"m" + str(datetime.now().month) + "d" + str(datetime.now().day) + ".txt", 'w') as f:
                f.write(str(result))
            break

    print('end loop for', gpdm)

    itchat.logout()

from threading import Thread

for i in stock_l:
    t = Thread(target=jiance, args=(i,))
    t.start()



# print(itchat.search_chatrooms(name="triple_group"))