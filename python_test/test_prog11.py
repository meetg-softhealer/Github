
def WordSplit(strArr):
    str1 = strArr[0]
    strArr.remove(strArr[0])
    strArr = strArr[0]
    x = strArr.split(",")
    result = []

    for i in x:
        if i in str1 and i!=str1[:len(i)]:
            a = len(str1)
            b = len(i)
            
            result.append(str1[:a-b])
            result.append(i)
        else:
            pass
    
    print(result)

x = ["hellocat", "apple,bat,cat,goodbye,hello,yellow,why"]
WordSplit(x)