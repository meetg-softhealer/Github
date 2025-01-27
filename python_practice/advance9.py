dt = {7:8, 1:9, 6:3}
l1 = []
l2 = []

l1.append(dt.keys())
l2.append(dt.values())

def myfunc(l2):
    return l2


print(l1)
l1.sort(key=myfunc)
print(l1)

