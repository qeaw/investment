import os, os.path
import requests
import tushare as ts

def chajing(s):
    return s[:2].upper() + "#" + s[2:] + ".txt"

def huifu(w):
    return w[:2] + w[3:9]

def huifushuzi(w):
    return w[3:9]


today = "2017-09-29"
def huice(wenjianming,today):
    os.chdir(r"C:\Users\qeaw\Desktop\test\monipan")
    if os.path.isdir(wenjianming):
        pass
    else:
        x = ts.get_hist_data(huifushuzi(wenjianming),today).loc[today]["open"]
        with open(wenjianming,"w") as f:
            f.write(f"{today}\t{x}")

w = "SZ300189"

huice(chajing(w),today)
