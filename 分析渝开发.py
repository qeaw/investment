#-*- coding=utf-8 -*-
from __future__ import division
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import pandas.util.testing as tm
import statsmodels
import statsmodels.api as sm
import math
import matplotlib.pyplot as plt
# from statsmodels.tsa.stattools import grangetcausalitytests as granger
import os
import glob
import sys
import codecs
import ch
ch.set_ch()


def timelyvar(dir):
    """give two date for the start and end period for calculate var"""
    if not os.path.isdir(dir):
        print "%s not a directory" % dir
        return False

    for txtFile in glob.glob(os.path.join(dir,"SZ000514.txt")):
        datadf = pd.read_table(txtFile, skiprows=2, skipfooter=1, header=None, engine='python',
                               parse_dates=False)
        row1 = pd.read_table(txtFile, nrows=3, encoding='gbk')
        stocknum = row1.columns[0][:6]
        days = 30
        outdata = 0
        outnum = []
        result_list = []
        stock_list = []
        if len(datadf.index) < days:
            # print stocknum,"provide too less data to analyse"
            outdata += 1
            outnum.append(stocknum)
            continue
        else:
            datadf.columns = ['date', 'open', 'high', 'low', 'end', 'quantity', 'valume']
            d2 = datadf.set_index('date')
            d2.columns.name = stocknum
            d3 = DataFrame(d2, columns=['end', 'quantity'])

            end_price = Series(d3["end"])
            end_quan = Series(d3['quantity'])

            if '05/18/2016' not in end_price.index:
                print stocknum, "not trading by start date"
                continue
            if '10/31/2016' not in end_price.index:
                print stocknum, 'not trading by end date'
                continue



            end_price_m = end_price['05/18/2016':'10/31/2016']
            end_quan_m = end_quan['05/18/2016':'10/31/2016']

            var = end_price_m.var() / (end_price_m.mean() ** 2)
            return var
            # stock_list.append(stocknum)
            # result_list.append(var)
            #

    # dic = {"number": stock_list,
    #        "var": result_list}
    # data = DataFrame(dic, columns=["number", "var"])
    # output = data.set_index("number")
    #
    # return output.sort_values(by="var", ascending=True)

def process_var(dir,days):
    """take a dir and an int to be the exam period from now. return a series with stock number be the index, the var of price(modified) to be the value."""
    if not os.path.isdir(dir):
        print "%s not a directory" % dir
        return False
    days = int(days)
    dic = {}

    outdata = 0
    outnum = []
    for txtFile in glob.glob(os.path.join(dir,"*.txt")):
        # print txtFile
        datadf = pd.read_table(txtFile, skiprows=2, skipfooter=1, header=None, engine='python',
                               parse_dates=False)
        row1 = pd.read_table(txtFile, nrows=3, encoding='gbk')
        stocknum = row1.columns[0][:6]
        if len(datadf.index) < days :
            # print stocknum,"provide too less data to analyse"
            outdata +=1
            outnum.append(stocknum)
            continue
        else:
            datadf.columns = ['date', 'open', 'high', 'low', 'end', 'quantity', 'valume']
            d2 = datadf.set_index('date')
            d2.columns.name = stocknum
            d3 = DataFrame(d2, columns=['end', 'quantity'])[-days:]



            end_price = Series(d3["end"])
            end_quan = Series(d3['quantity'])

            

            price_m =end_price * end_quan

            # price_m_m = price_m / end_quan.mean()
            # vwap = price_m.sum() / end_quan.sum()


            # var = ((end_price - vwap) ** 2).sum() / len(end_price)

            var = end_price.var()
            # std = price_m_m.std()
            # std_m = std / end_price.mean()
            var_m = var / end_price.mean() ** 2
            # print var_m

            dic[stocknum] = var_m


    output = Series(dic)

    print 'there are', days, "days"
    print outdata, 'are rule out for too short data'
    print "others modified var:"


    return output.sort_values(ascending=True)








dir = r"C:\Users\qeaw\Desktop\DATA\dd"

ykfvar = timelyvar(dir)
all_stock = process_var(dir,166)
smaller = all_stock[all_stock < ykfvar]

print len(all_stock)
print len(smaller)
print smaller