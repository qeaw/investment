import tushare as ts
import os

def find2017():
    r2017 = ts.get_report_data(2017,3).set_index("code")
    r2016 = ts.get_report_data(2016,4).set_index("code")
    l = []
    l1= []
    for i in r2017.index:
        if i not in r2016.index:
            continue
        rate = (r2017.net_profits[i] - r2016.net_profits[i]) / r2016.net_profits[i]

        try:
            rate = float(rate)
        except:
            rate = rate.values[0]
        if rate > 0.25:
          # l.append((rate,i))
          l1.append(i)
    print(l1)

    r2015 = ts.get_report_data(2015, 4).set_index("code")

    l2 = []
    for i in l1:
        if i not in r2015.index:
            continue
        rate = (r2016.net_profits[i] - r2015.net_profits[i]) / r2015.net_profits[i]

        try:
            rate = float(rate)
        except:
            rate = rate.values[0]
        if rate > 0.3:
            # ll.append((l1[i],rate, i))
            l2.append(i)
    r2014 = ts.get_report_data(2014, 4).set_index("code")
    print(l2)
    l3 = []
    for i in l2:
        if i not in r2014.index:
            continue
        rate = (r2015.net_profits[i] - r2014.net_profits[i]) / r2014.net_profits[i]

        try:
            rate = float(rate)
        except:
            rate = rate.values[0]
        if rate > 0.3:
            # ll.append((l1[i],rate, i))
            l3.append(i)
    print(l3)
    return l3

result = find2017()

os.chdir(r"C:\Users\qeaw\Desktop\rrr")

with open("3.txt","w") as f:
    f.write(str(result))