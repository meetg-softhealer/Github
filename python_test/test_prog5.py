list1 = [1, 2, 3, 4, 5, 6]
pos = 3
def rotate_list(l1, pos):
    demo = []
    n = len(l1)
    for i in range(pos):
        demo.append(l1[n-i-1])
        l1.remove(l1[n-i-1])
    demo.reverse()
    print(demo+l1)
    
rotate_list(list1,pos)

