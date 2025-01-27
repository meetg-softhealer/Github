str1 = "aabbbccde"
x = []
y = 0
for i in str1:
    x.append(i)

dict1 = dict.fromkeys(x,y)

for i in str1:
    if i in dict1.keys():
        dict1[i] = dict1[i] + 1

print(dict1)
