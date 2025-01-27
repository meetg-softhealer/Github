l1 = ["a","e","i","o","u"]

str1 = "hello world"
str1_list = [x for x in str1]

l2 = []
l3 = []
for i in range(len(str1)):
    if str1[i] in l1:
        l2.append(str1[i])
        l3.append(i)
    else:
        pass

l2.reverse()

for i in range(len(l2)):
    str1_list[l3[i]] = l2[i]

result = ""
for i in str1_list:
    result = result + i


print(result)