list1 = [10, 20, 30, 10, 10, 20, 40, 50]
y = 0

dict1 = dict.fromkeys(list1,0)

for i in range(len(list1)):
    if list1[i] in dict1.keys():
        dict1[list1[i]] = dict1[list1[i]] + 1


for key,value in dict1.items():
    print(key,"appears",value,"times.")