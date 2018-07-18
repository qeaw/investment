import tushare as ts
import os


def huifushuzi(w):
    return w[3:9]


def find_sh(gpdm):
    x = ts.get_hist_data(gpdm)

    if x.loc["2017-11-15"].p_change > 0 and x.loc["2017-10-30"].p_change > 0 and x.loc["2017-09-07"].p_change > 0:
        return gpdm

def find_zxb(gpdm):
    x = ts.get_hist_data(gpdm)

    if x.loc["2017-11-17"].p_change > 0 and x.loc["2017-11-15"].p_change > 0 and x.loc["2017-11-14"].p_change > 0:
        return gpdm

def find_cyb(gpdm):
    x = ts.get_hist_data(gpdm)

    if x.loc["2017-11-17"].p_change > 0 and x.loc["2017-10-16"].p_change > 0 and x.loc["2017-10-30"].p_change > 0:
        return gpdm





result = []

for i in os.listdir(r"C:\stock_data"):
    if i[3] == "3":
        try:
            x = find_cyb(huifushuzi(i))
            if type(x) == str:
                result.append(x)
                print(f"{x} added")
        except:
            print(f"{huifushuzi(i)}not in")
    if i[5] == "2":
        try:
            x = find_zxb(huifushuzi(i))
            if type(x) == str:
                result.append(x)
                print(f"{x} added")
        except:
            print(f"{huifushuzi(i)}not in")
    else:
        try:
            x = find_sh(huifushuzi(i))
            if type(x) == str:
                result.append(x)
                print(f"{x} added")
        except:
            print(f"{huifushuzi(i)}not in")


print(result)
os.chdir(r"C:\Users\qeaw\Desktop\rrr\2017-11-18")
with open("jieguo2.txt","w") as f:
    f.write(str(result))