import tushare as ts
import os
import pandas as pd
df = ts.fund_holdings(2017,3)
jdf = ts.fund_holdings(2017,3)
# jdf = ts.fund_holdings(2017,2)

df2 = df.set_index("code")
jdf2 = jdf.set_index("code")
# jdf2 = jdf.set_index("code")

df2["ratio_change"] = df2.ratio.astype("float") - jdf2.ratio.astype("float")

df2.ratio = df2.ratio.astype("float")
df2.clast = df2.clast.astype("float")
df3 = df2.sort_values(by = "clast", ascending=False)


#
ndf = pd.DataFrame(index=df3.index,columns=["price_change1","price_change2"])
for i in df3.index:

    x = ts.get_k_data(i,autype="qfq")
    if len(x)<100:
        continue
    ndf["price_change1"][i] =(x.close[len(x)-16] -  x.close[len(x)-82]) / x.close[len(x)-82]
    ndf["price_change2"][i] =(x.close[len(x)-1] -  x.close[len(x)-16]) / x.close[len(x)-16]

df3["price_change1"] = ndf["price_change1"]
df3["price_change2"] = ndf["price_change2"]





print(df3[:20])
df3.to_csv(r"C:\Users\qeaw\Desktop\rrr\2017-10-29\result2.csv")