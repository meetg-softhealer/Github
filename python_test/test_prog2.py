list1 = [("Alice", 25), ("Bob", 35), ("Charlie", 30)]
for i in range(len(list1)):
    list1[i] = list(list1[i])


def names(l1):
    l2 = []
    for i in range(len(l1)):
        if l1[i][1]>=30:
            l2.append(l1[i][0])  
    return l2

print(names(list1))