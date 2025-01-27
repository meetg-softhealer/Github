num = [2,3,6,6,5]
n = len(num)
num.sort()

if num[n-1]==num[n-2]:
    print(num[n-3])
else:
    print(num[n-1])

    

