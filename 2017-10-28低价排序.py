import tushare as ts
import requests
import os

df = ts.fund_holdings(2017,3)

df.clast = df.clast.astype("float")

df2 = df.set_index("code")

def chajing(s):
    return s[:2].upper() + "#" + s[2:]

def huifushuzi(w):
    return w[3:9]

def huifu(w):
    return w[0:2].lower() + w[3:9]

def zhao(gpdm):
    x = ts.get_k_data(gpdm, autype="hfq")
    if type(x) == type(None):
        return
    if len(x) < 150:
        return
    if x.close[len(x)-100] * 1.2 > x.close[len(x) - 1]:
        return gpdm

ll = []
lll = []
for i in os.listdir(r"C:\stock_data"):
    jieguo = zhao(huifushuzi(i))
    if type(jieguo) == str:
        ll.append(jieguo)
        print(f"{jieguo}appended")
# df = df.reindex(index = ll)

for i in ll:
    try:
        lll.append(list(df2.loc[i]))
    except KeyError:
        print(f"jumped {i}")



d = sorted(lll,key=lambda s:float(s[4]),reverse=True)

print(d[:15])