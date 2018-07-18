import tushare as ts
import requests
import os
from datetime import datetime
import numpy
from time import sleep
def chajing(s):
    return s[:2].upper() + "#" + s[2:]

def huifushuzi(w):
    return w[3:9]

def huifu(w):
    return w[0:2].lower() + w[3:9]

def jiance(gpdm,pb = 1,ps = 1,vb = 1,vs = 1):
    jl = junliang(gpdm)
    with open(f"{gpdm}-{datetime.now().date()}.txt", "a") as f:
        print(f"{gpdm}最近三天均量为{jl}")
        f.write(f"{gpdm}最近三交易日大单均值{jl}\n")

    while datetime.now().hour < 15:
        r = ts.get_realtime_quotes(gpdm)
        pn = float(r.price[0])
        # print(r.b5_v[0])
        zheng = 0
        fu = 0
        # print(r.b1_v[0],r.b2_v[0],r.b3_v[0],r.b5_v[0],r.b1_v[0],)
        if r.b1_v[0].isdigit():
            zheng += float(r.b1_v[0])
            # print("买一",r.b1_v[0])
        if r.b2_v[0].isdigit():
            zheng += float(r.b2_v[0])
            # print("买2", r.b2_v[0])
        if r.b3_v[0].isdigit():

            zheng += float(r.b3_v[0])
        if r.b4_v[0].isdigit():
            zheng += float(r.b4_v[0])
        if r.b5_v[0].isdigit():
            zheng += float(r.b5_v[0])
        if r.a1_v[0].isdigit():

            fu += float(r.a1_v[0])
        if r.a2_v[0].isdigit():
            fu += float(r.a2_v[0])

        if r.a3_v[0].isdigit():
            fu += float(r.a3_v[0])
        if r.a4_v[0].isdigit():
            fu += float(r.a4_v[0])
        if r.a5_v[0].isdigit():
            fu += float(r.a5_v[0])

        # liangbi = (float(r.b1_v[0]) + float(r.b2_v[0]) + float(r.b3_v[0]) + float(r.b4_v[0]) + float(r.b5_v[0])) / (float(r.a1_v[0]) + float(r.a2_v[0]) + float(r.a3_v[0]) + float(r.a4_v[0]) + float(r.a5_v[0]))

        if zheng == 0 or fu == 0:
            continue
        liangbi = zheng / fu
        print(datetime.now(),gpdm,liangbi,zheng,fu)

        if liangbi > 10 and (abs(pb - pn) / pb > 0.01 or liangbi > vb * 1.5) and max(zheng,fu) > jl:
            with open(f"{gpdm}-{datetime.now().date()}.txt", "a") as f:
                line = f"{datetime.now()}\t买入\t{pn}\t{round(liangbi,2)}\t{zheng}\t{fu}\n"
                print(line)
                f.write(line)
            pb = pn
            vb = liangbi
        if liangbi < 0.1 and (abs(ps - pn) / ps > 0.01 or liangbi < vs / 1.5) and max(zheng,fu) > jl:
            with open(f"{gpdm}-{datetime.now().date()}.txt", "a") as f:
                line = f"{datetime.now()}\t卖出\t{pn}\t{round(1/liangbi,2)}\t{zheng}\t{fu}\n"
                print(line)
                f.write(line)
            ps = pn
            vs = liangbi
        sleep(1)



def junliang(gpdm):
    now = datetime.now()
    w = now.weekday()
    if w == 0:
        y1 = f"{now.year}-{now.month}-{now.day-3}"
        y2 = f"{now.year}-{now.month}-{now.day-4}"
        y3 = f"{now.year}-{now.month}-{now.day-5}"
    if w == 1:
        y1 = f"{now.year}-{now.month}-{now.day-1}"
        y2 = f"{now.year}-{now.month}-{now.day-4}"
        y3 = f"{now.year}-{now.month}-{now.day-5}"
    if w == 2:
        y1 = f"{now.year}-{now.month}-{now.day-1}"
        y2 = f"{now.year}-{now.month}-{now.day-2}"
        y3 = f"{now.year}-{now.month}-{now.day-5}"
    if w >= 3:
        y1 = f"{now.year}-{now.month}-{now.day-1}"
        y2 = f"{now.year}-{now.month}-{now.day-2}"
        y3 = f"{now.year}-{now.month}-{now.day-3}"


    jl = 0
    n = 0
    for i in [y1,y2,y3]:
        df = ts.get_sina_dd(gpdm,i,vol=100)

        if df is None:
            continue
        if len(df) < 10:
            jl += df.volume.mean()
            n += 1
        if len(df) >= 10:
            jl += df.sort_values(by = "volume", ascending=False).volume[:10].mean()
            n += 1
    if n == 0:
        return 0
    jl = jl / n
    jl = jl / 100
    return jl


os.chdir(r"C:\Users\qeaw\Desktop\rrr\liangbijieguo")

gpdms = ["603025","300052","600391","600526","600380",
         "300480","300615","300220","300593","000559",
         "600770","603177",'600626',"300568"]
gpdm = "600770"
# jiance(gpdm)

from threading import Thread
#
for i in gpdms:
    t = Thread(target=jiance, args=(i,))
    t.start()
#
