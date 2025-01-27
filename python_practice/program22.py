dic1 = {
'list1' : {'id': 123 ,'name': 'ABC' , 'sequence': 5},
'list2' : {'id': 124 ,'name': 'DEF' , 'sequence': 4},
'list3' : {'id': 125 ,'name': 'XYZ' , 'sequence': 1},
'list4' : {'id': 126 ,'name': 'MNO' ,'sequence':  3},
'list5' : {'id': 127 ,'name': 'PQR' , 'sequence': 2}
}
# print(dic1[])
lists=[]
for key,val in dic1.items():
    for keys,vals in val.items():
        if keys=='sequence':    
            lists.append(vals)
lists.sort()
for i in range(len(lists)):
    for key,val in dic1.items():
        for keys,vals in val.items():
            if keys=='sequence' and vals==lists[i]:    
                print(key,dic1[key])
                
                
                
sorted_dictionary=dict(sorted(dic1.items(),key=lambda vals:vals[1]['sequence']))
print(sorted_dictionary)