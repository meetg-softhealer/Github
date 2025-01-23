list1 = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
list2 = [0,1,1,0,1,2,2,0,1]


#['a', 'd', 'h', 'b', 'c', 'e', 'i', 'f', 'g']
list3 = []

for i in range(len(list1)):
    list3.append([list2[i],list1[i]])

list3.sort()

list4 = []

for i in range(len(list3)):
    list4.append(list3[i][1])

print(list4)




