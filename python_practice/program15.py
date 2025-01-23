my_list = [1,[1.1,2,[3],6],7,9,[5.6,[8]],9]

index = 0
for i in my_list:
    x = str(type(i))

    if "list" in x:
        my_list.remove(i)
        j_ctr = 0
        for j in i:
            my_list.insert(index+j_ctr, j)
            j_ctr = j_ctr + 1
    
    index = index + 1

print(my_list)
#output = [1,1.1,2,3,6,7,9,5.6,8,9]