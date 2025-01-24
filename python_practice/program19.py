x = [(), (), ('',), ('a', 'b'), ('a', 'b', 'c'), ('d')]
y = []
for i in range(len(x)):
    if (len(x[i])<1):
        y.append(x[i])

for i in y:
    x.remove(i)

print(x)