dict1 = {'a': 1, 'b': 2, 'c': 3}
list1 = list(dict1.keys())
list2 = list(dict1.values())

dict2 = {}

for x in range(len(list1)):
    dict2[list2[x]] = list1[x]


print(dict2)