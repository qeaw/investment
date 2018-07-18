import os

f = open(r"C:\Users\qeaw\Desktop\test\lambda\result.txt","r")

xx = f.readlines()
result = []
for x in xx:
    x = x.split("\t")
    gpdm = x[0]
    l1 = float(x[1])
    l2 = float(x[2])
    # print(gpdm,l1,l2)
    result.append((gpdm,l1,l2))

r1 =  result.copy()
r2 = result.copy()

r1.sort(key= lambda s:s[1],reverse= True)

r2.sort(key = lambda s: s[2])

print(r1[:10])
print(r2[:10])

for i in r1[:100]:
    if i in r2[:100]:
        print(f"交集:{i}")
