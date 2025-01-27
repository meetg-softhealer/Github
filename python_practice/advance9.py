dt = {7:8, 1:9, 6:3}
lists=[]
sorted_dictionary={}
for key,val in dt.items():   
        lists.append(val)
lists.sort()
for i in range(len(lists)):
    for key,val in dt.items():
        if val==lists[i]:    
            sorted_dictionary[key]=val
            # print(f"{key}:{val}")
print(sorted_dictionary)
            
sorted_dictionary=dict(sorted(dt.items(),key=lambda val:val[1]))
print(sorted_dictionary)