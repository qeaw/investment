import tkinter,time
import requests
import os
# from tkinter import Tk,Button,mainloop
import numpy as np
import pandas as pd
import smtplib
from email.mime.text import MIMEText

from pandas import DataFrame, Series
from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta


# zqb = sz300052
# thfw = sz300008
os.chdir("C:\stock_data")
datadf = pd.read_table("SZ#300052.txt", skiprows=2, skipfooter=1, header=None, engine='python',
                               parse_dates=False)
# print(datadf)

data30 = datadf.ix[len(datadf[6])-30:]
vol30 = data30[6]
sorted30 = data30.sort_values(by = 6)[6]
minmean = sorted30[:5].mean()
maxmean = sorted30[25:].mean()
print(minmean,maxmean)
def show(content):
    # messagebox.showinfo(title = 'quantity remaind', message = content)
    pass

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

_user = "2458742185@qq.com"
_pwd  = "ewhomfvvurmndifi"
_to   = "407129740@qq.com"

def print_daxie(number):
    num = int(number)
    num_str = str(num)
    leng = len(num_str)
    wei = ["元","十","百","千","万","十万","百万","千万","亿","十亿","百亿"]
    result = num_str[0] + wei[len(num_str) -1]
    print(q,result)
result = []
while True:
    now = datetime.now()
    r = requests.get('http://hq.sinajs.cn/list=sz300052')
    q = int(float(r.text.split(',')[9]))
    p = float(r.text.split(',')[3])

    print(datetime.now())
    print_daxie(q)
    # send_email(_user,_pwd,_to,"volume remaind", f"current volume{q}")
    if now.hour == 10 and now.minute == 0:
        predq = q * 8
        if predq > maxmean:
            send_email(_user, _pwd, _to, "volume remaind", f"sell: current volume {q}")
            show(f"sell for predicted quantity is high at {predq}")
            result.append([q,p,now,"sell"])
        if predq < minmean:
            send_email(_user, _pwd, _to, "volume remaind", f"buy: current volume {q}")
            show(f"buy for predicted quantity is low at {predq}")
            result.append([q, p, now,"buy"])
    if now.hour == 11 and now.minute == 0:
        predq = q * 8 / 3
        if predq > maxmean:
            send_email(_user, _pwd, _to, "volume remaind", f"sell: current volume {q}")
            show(f"sell for predicted quantity is high at {predq}")
            result.append([q, p, now, "sell"])
        if predq < minmean:
            send_email(_user, _pwd, _to, "volume remaind", f"buy: current volume {q}")
            show(f"buy for predicted quantity is low at {predq}")
            result.append([q, p, now,"buy"])
    if now.hour == 13 and now.minute == 30:
        predq = q * 8 / 5
        if predq > maxmean:
            send_email(_user, _pwd, _to, "volume remaind", f"sell: current volume {q}")
            show(f"sell for predicted quantity is high at {predq}")
            result.append([q, p, now, "sell"])
        if predq < minmean:
            send_email(_user, _pwd, _to, "volume remaind", f"buy: current volume {q}")
            show(f"buy for predicted quantity is low at {predq}")
            result.append([q, p, now,"buy"])
    if now.hour == 14 and now.minute == 30:
        predq = q * 8 / 7
        if predq > maxmean:
            send_email(_user, _pwd, _to, "volume remaind", f"sell: current volume {q}")
            show(f"sell for predicted quantity is high at {predq}")
            result.append([q, p, now, "sell"])
        if predq < minmean:
            send_email(_user, _pwd, _to, "volume remaind", f"buy: current volume {q}")
            show(f"buy for predicted quantity is low at {predq}")
            result.append([q, p, now,"buy"])
    if q > maxmean:
        send_email(_user, _pwd, _to, "volume remaind", f"sell :current volume {q}")
        show(f"sell for predicted quantity is high at {q}")
        result.append([q, p, now, "sell"])
    # if q < minmean:
    #     send_email(_user, _pwd, _to, "volume remaind", f"buy:current volume {q}")
    #     show(f"buy for predicted quantity is low at {q}")
    #     result.append([q, p, now,"buy"])
    time.sleep(59)
    if now.hour >= 15:
        os.chdir(r'C:\Users\qeaw\Desktop\test')
        with open('zqb'+str(datetime.now().day) + ".txt", 'w') as f:
            f.write(str(result))
        break

print('end loop')











# mean30 = int(datadf[6][len(datadf[6])-30:].mean())

