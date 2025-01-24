tup = [10,20,30,(10,20),40]
ctr = 0
for i in tup:
    if "tuple" not in str(type(i)):
        ctr = ctr + 1
print(ctr)