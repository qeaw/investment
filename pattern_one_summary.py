import os

os.chdir(r"C:\Users\qeaw\Desktop\test\monipan")
r = []
for i in os.listdir():
    l = []
    with open(i,"r") as f:
        x = f.readlines()
        for xx in x:
            xx = xx.split("\t")
            l.append((xx[0],float(xx[-1][:len(xx[-1])-1])))
    # print(i)
    na = i[:6]
    n =r"C:\Users\qeaw\Desktop\test\monipanjieguo" + "\\" +  "jieguo.txt"
    # print(name)
    b= []
    b_number = 0
    b_linshi = 0
    result = 1
    for i in l:
        if i[0] == "buy":
            b.append(i[1])
            # b_number += 1
            b_linshi += 1
        if i[0] == "sell":
            result *= (i[1] / sum(b)) * b_linshi
            b_linshi = 0
    # print(result)
    with open(n,"a") as f:
        ss = f"{na}\t{result}\n"
        f.write(ss)
    r.append(result)


os.chdir(r"C:\Users\qeaw\Desktop\test\monipanjieguo")
yidang = 0
erdang = 0
sandang = 0
sidang = 0
wudang = 0

for i in r:
    if i < 1:
        yidang += 1
    elif i >= 1 and i < 1.2:
        erdang += 1
    elif i < 1.4 and i >= 1.2:
        sandang += 1
    elif i < 1.6 and i >=1.4:
        sidang += 1
    elif i > 1.6:
        wudang += 1

jieguo = f"亏损：{yidang}\n1-1.2:{erdang}\n1.2-1.4:{sandang}\n1.4-1.6:{sidang}\n1.6 above:{wudang}\n总：{sum(r) / len(r)}"

print(jieguo)


with open("sumary.txt","w") as f:
    f.write(jieguo)

