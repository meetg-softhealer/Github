import sys
list1 = []

while True:
    x = input("Enter num:-")
    if x=='q' or x=='Q': break
    list1.append(int(x))

list1.sort()
print(list1[0])
print(list1[len(list1)-1])

closest = sys.maxsize
longest = 0

for i in range(len(list1)):
    for j in range(len(list1)):
        if i==j : continue
        x = abs(i-j)
        if(x<closest):
            closest = x
        elif(x>longest):
            longest = x

print(closest)
print(longest)

print(sum(list1))
print(sum(list1)/len(list1))

