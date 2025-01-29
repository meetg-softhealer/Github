x = "abc"
y = 100

try:
    print(x+y)
except:
    raise TypeError("String and Integer cannot be concatenated together.")


try:
    print(y/0)
except:
    raise ZeroDivisionError("Any number cannot be divided by 0")


try: 
    print(i)
except:
    raise AssertionError("The variable cannote be accessed as it's not present") 