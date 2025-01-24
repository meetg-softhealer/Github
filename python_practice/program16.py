my_list = [3,8,5,4,6,3,1]

list1 = []

for i in range(len(my_list)-1):
    list2 = []
    if my_list[i]+my_list[i+1]==9:
        list2.append(i)
        list2.append(i+1)
        list1.append(list2)

print(list1)