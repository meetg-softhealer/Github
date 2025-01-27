num = [5, 10, 10]
n = len(num)
num.sort()

if num[n-1]==num[n-2]:
    print(num[n-3])
else:
    print(num[n-1])