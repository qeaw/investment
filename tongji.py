import os
import pandas as pd

os.chdir(r"C:\Users\qeaw\Desktop\rrr\result4")

fu = 0
yi = 0
er = 0
san = 0
si = 0
chao = 0
fj = []

for i in os.listdir():
    f = open(i,"r")
    s = f.read()
    sl = s.split("：")
    sy = float(sl[2][:-5])

    if sy == "nan":
        pass
    if sy<1:
        fu += 1
        fj.append(i)
        print(i)
    if sy>1 and sy<=1.5:
        yi += 1
    if  sy>1.5and sy<=2 :
        er += 1
    if sy>2 and sy<2.5:
        san += 1
    if sy>2.5 and sy<3:
        si += 1
    if sy>3:
        chao += 1

print(f"负收益:{fu}\n 收益1-1.5:{yi}\n 收益1.5-2:{er}\n 收益2-2.5:{san}\n 收益2-3:{si}\n 收益超过3:{chao}")

os.chdir(r"C:\Users\qeaw\Desktop\tongji")
with open(r"result2.txt","w") as f:
    f.write(f"负收益:{fu}\n 收益1-1.5:{yi}\n 收益1.5-2:{er}\n 收益2-2.5:{san}\n 收益2-3:{si}\n 收益超过3:{chao}")

with open(r"fude2.txt","w") as f:
    f.write(f"负收益:{fj}")
