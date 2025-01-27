dict1 = {'a': [1, 2, 3], 'b': [2, 3, 4], 'c': [2, 3, 4]}

my_list = []
for x in dict1.values():
    my_list.append(x)

for j in my_list[0]:
    if j in my_list[1] and my_list[2]:
        print(j)
        break

