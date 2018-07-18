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




stock_l2 = [["sh603177",20.5,25],["sz300615",32.5,42.5],["sh600526",11.5,12.5],
["sh600604",8.2,9.5],["sz002268",22,26.5],["sz000559",11.5,12.5],
["sh600526",10.5,12.5],["sz300538",45,50],["sh603996",18.5,22.5],["sz300052",14.5,16.5]]
#with open("config.txt","r") as f:
#    r = f.readlines()
#stock_l2 = eval(r[0])

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
_pwd = "ewhomfvvurmndifi"
_to = "407129740@qq.com"

def jiance(gpdm,pb,ps):

    if datetime.now().hour < 9:
        print(f"sleep{(datetime.now().replace(hour=9,minute=25) - datetime.now()).seconds}seconds,{(datetime.now().replace(hour=9,minute=25) - datetime.now()).seconds / 60} minutes")
        time.sleep((datetime.now().replace(hour=9,minute=25) - datetime.now()).seconds)
    if datetime.now().hour > 11 and datetime.now().hour < 13:
        print(f"sleep{(datetime.now().replace(hour=13,minute=0) - datetime.now()).seconds}seconds,{(datetime.now().replace(hour=13,minute=0) - datetime.now()).seconds / 60} minutes")
        time.sleep((datetime.now().replace(hour=13,minute=0) - datetime.now()).seconds)


    gpdms = gpdm[2:]


    #
    datadf = ts.get_k_data(gpdms,autype="qfq")
    #
    if type(datadf) == type(None):
        print(gpdm,"NoneType")
        return
    if len(datadf) < 100:
        print(gpdm,"duan")
        return


    # now = datetime.now()
    # x = datetime.strptime(datadf.date[datadf.index[0] +len(datadf) - 1], "%Y-%m-%d")
    # # print(gpdm,datadf.index[0])
    # if (now - x).days > 15:
    #     print(gpdm,"tingpan")
    #     return

    # qnow = datadf.volume[datadf.index[datadf.index[0] + len(datadf) - 1]]
    # pnow = datadf.close[datadf.index[datadf.index[0] + len(datadf) - 1]]
    minmean = datadf.volume[datadf.index[datadf.index[0] + len(datadf) - 45]:datadf.index[datadf.index[0] + len(datadf) - 1]].min()
    maxmean = sum(sorted(datadf.volume[datadf.index[datadf.index[0] + len(datadf) - 45]:datadf.index[datadf.index[0] + len(datadf) - 1]])[42:]) / 3
    n = 0
    result = []
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

        if now.hour == 9 and now.minute == 45:
            predq = v * 16
            if predq > maxmean or p > ps:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "sell"])
            if predq < minmean or p < pb:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "buy"])
        if now.hour == 10 and now.minute == 0:
            predq = v * 16 / 2
            if predq > maxmean or p > ps:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "sell"])
            if predq < minmean or p < pb:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "buy"])
        if now.hour == 10 and now.minute == 15:
            predq = v * 16 / 3
            if predq > maxmean or p > ps:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "sell"])
            if predq < minmean or p < pb:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "buy"])
        if now.hour == 10 and now.minute == 30:
            predq = v * 16 / 4
            if predq > maxmean or p > ps:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "sell"])
            if predq < minmean or p < pb:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "buy"])
        if now.hour == 10 and now.minute == 45:
            predq = v * 16 / 5
            if predq > maxmean or p > ps:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "sell"])
            if predq < minmean or p < pb:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "buy"])
        if now.hour == 11 and now.minute == 0:
            predq = v * 16 / 6
            if predq > maxmean or p > ps:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "sell"])
            if predq < minmean or p < pb:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "buy"])
        if now.hour == 11 and now.minute == 15:
            predq = v * 16 / 7
            if predq > maxmean or p > ps:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "sell"])
            if predq < minmean or p < pb:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "buy"])


        if now.hour == 11 and now.minute == 25:
            predq = v * 16 / 8
            if predq > maxmean or p > ps:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "sell"])
            if predq < minmean or p < pb:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "buy"])
        if now.hour == 13 and now.minute == 15:
            predq = v * 16 / 9
            if predq > maxmean or p > ps:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "sell"])
            if predq < minmean or p < pb:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "buy"])

        if now.hour == 13 and now.minute == 30:
            predq = v * 16 / 10
            if predq > maxmean or p > ps:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "sell"])
            if predq < minmean or p < pb:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "buy"])
        if now.hour == 13 and now.minute == 45:
            predq = v * 16 / 11
            if predq > maxmean or p > ps:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "sell"])
            if predq < minmean or p < pb:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "buy"])
        if now.hour == 14 and now.minute == 0:
            predq = v * 16 / 12
            if predq > maxmean or p > ps:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "sell"])
            if predq < minmean or p < pb:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "buy"])
        if now.hour == 14 and now.minute == 15:
            predq = v * 16 / 13
            if predq > maxmean or p > ps:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "sell"])
            if predq < minmean or p < pb:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "buy"])
        if now.hour == 14 and now.minute == 30:
            predq = v * 16 / 14
            if predq > maxmean or p > ps:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "sell"])
            if predq < minmean or p < pb:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "buy"])
        if now.hour == 14 and now.minute == 45:
            predq = v * 16 / 15
            if predq > maxmean or p > ps:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"卖出 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "sell"])
            if predq < minmean or p < pb:
                send_email(_user, _pwd, _to, "成交量提醒",
                           f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                # itchat.search_friends(name="禅语")[0].send(f"卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
                itchat.search_chatrooms(name="triple_group")[0].send(
                    f"买入 {name}{gpdms}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}")
                result.append([v, p, now, "buy"])
        if v > maxmean and n < 1:
            send_email(_user, _pwd, _to, "成交量提醒",
                       f"现在卖出 {name}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}, 量比{round(v / minmean,2)}")
            show(f"sell for predicted quantity is high at {v}")
            # itchat.search_friends(name="禅语")[0].send(f"现在卖出 {name}{gpdm}: 现成交量 {daxie(q)}, 现价{p}, 涨幅{rate}, 量比{round(q / minmean,2)}")
            itchat.search_chatrooms(name="triple_group")[0].send(
                f"现在卖出 {name}{gpdm}: 现成交量 {daxie(v)}, 现价{p}, 涨幅{rate}, 量比{round(v / minmean,2)}(之后不再提醒)")
            result.append([v, p, now, "sell"])
            n += 1
        time.sleep(59)

        if now.hour >= 15:
            # os.chdir(r'C:\Users\qeaw\Desktop\test')
            with open(gpdm + "m" + str(datetime.now().month) + "d" + str(datetime.now().day) + ".txt", 'w') as f:
               f.write(str(result))
            break

    print('end loop for', gpdm)

    itchat.logout()

from threading import Thread

for i in stock_l2:
    t = Thread(target=jiance, args=(i[0],i[1],i[2]))
    t.start()

