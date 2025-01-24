x = "abcdefgabc"
dict1 = {}

dict1 = dict.fromkeys(x, 0)

for i in x:
    if i in dict1.keys():
        dict1[i] = dict1[i] + 1
print(dict1)
