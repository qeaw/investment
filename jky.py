import tushare as ts
from datetime import datetime
import sys
def daxie(number):
    num = int(number)
    num_str = str(num)
    leng = len(num_str)
    wei = ["元", "十", "百", "千", "万", "十万", "百万", "千万", "亿", "十亿", "百亿"]
    result = num_str[0] + wei[len(num_str) - 1] + num_str[1] + wei[len(num_str) - 2]
    return result

while True:

    gpdm = input("输入股票代码：（输入结束退出程序）")
    if gpdm == "结束":
        break

    # qsrq = "2017-01-10"
    # jsrq = "2017-10-18"
    qsrq = input("输入起始日期：（yyyy-mm-dd）")
    jsrq = input("输入结束日期：（yyyy-mm-dd）")

    jky = ts.get_hist_data(gpdm, qsrq,jsrq)


    jky_1 = ts.get_k_data(gpdm,qsrq,jsrq,autype="qfq")
    jky_2 = ts.get_k_data(gpdm)
    n = datetime.now()
    now = f"{n.year}-{n.month}-{n.day}"

    if jsrq == now:

        jky_1.loc[len(jky_1) + jky_1.index[0]] = jky_2.loc[len(jky_2)-1]



    jky = jky.reindex(index = jky.index.sort_values())
    jky_1 = jky_1.set_index(keys = "date")

    turnover = sum(jky["turnover"]) / 100
    #
    total_volume = sum(jky["volume"])
    #
    jiaquanjia = 0


    for i in range(len(jky)):
        jiaquanjia += jky.volume[i] * jky_1.close[i]

    jiaquanjia /= total_volume

    total_volume *= jiaquanjia * 100
    #
    print(f"总换手：{turnover}\n总量：{daxie(total_volume)}\n均价：{jiaquanjia}")


sys.exit()