
x = [[12,7,3],[4,5,6],[7,8,9]]
y = [[5,8,1],[6,7,3],[4,5,9]]
z = [[0,8,4],[6,9,3],[9,1,9]]

def multiplier(num, a):
    b = [[0,0,0],[0,0,0],[0,0,0]]
    for i in range(len(a)):
        for j in range(len(a[i])):
            b[i][j] = a[i][j] * num
    return b

def sum(a,b):
    arr = [[0,0,0],[0,0,0],[0,0,0]]
    for i in range(len(a)):
        for j in range(len(b)):
            arr[i][j] = a[i][j] + b[i][j]
    return arr
#the result should be like 3Y + (X + 2Y) + (5Z + 4X)

result = sum(multiplier(3,y),sum(sum(x,multiplier(2,y)),sum(multiplier(5,z),multiplier(4,x))))

print(result)
