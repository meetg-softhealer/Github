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

for i in list1:
    for j in list1:
        if i==j : continue
        x = abs(i-j)
        if(x<closest):
            closest = x
            closest_num1 = i
            closest_num2 = j
        elif(x>longest):
            longest = x
            longest_num1 = i
            longest_num2 = j

print("closest numbers:", closest_num1 , closest_num2)

print("longest numbers:", longest_num1, longest_num2)

print(sum(list1))
print(sum(list1)/len(list1))

