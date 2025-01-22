x = [1,2,1,2,3,4,5,1,1,2,5,6,7,8,9,9]

duplicates = []
for i in range(len(x)):
    for j in range(len(x)):
        if i==j:
            continue
        else:
            if x[i]==x[j]:
                duplicates.append(x[i])

duplicates = set(duplicates)

print(duplicates)