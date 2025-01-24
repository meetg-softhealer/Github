l = [("x", 1), ("x", 2), ("x", 3), ("y", 1), ("y", 2), ("z", 1)]

dict1 = {}

key = []
value = []
for i in range(len(l)):
    key.append(l[i][0])
    value.append(l[i][1])
    
for i in range(len(key)):
    dict1.update({key[i]:value[i]})

print(dict1)
    