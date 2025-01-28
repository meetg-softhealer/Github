
def valid_sequence(l1):
    b = False

    if len(l1)>=3 and len(l1)<14:
        for i in range(1,len(l1)):
            if l1[i]-1 == l1[i-1]:
                b = True
            else: 
                b = False
                break    
    
    
    return b

x = [1,2,3,4,5,6,7,8,9,10,11,12,13]

print(valid_sequence(x))