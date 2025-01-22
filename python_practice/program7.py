import sys
Input = [3, 9, 50, 15, 99, 7, 98, 65]

closest = sys.maxsize
for i in Input:
    for j in Input:
        if i==j : continue
        x = abs(i-j)
        if(x<closest):
            closest = x
            closest_num1 = i
            closest_num2 = j

print("closest numbers:", closest_num1 , closest_num2)

