dt = {7:8, 1:9, 6:3}
values=list(sorted(dt.values()))
i=0
for key,value in dt.items():
    dt[key] = values[i]
    i = i+1

    

print(dt)