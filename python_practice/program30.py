x = "abc"
y = 100

try:
    print(x+y)
except TypeError:
    raise Exception("String and Integer cannot be concatenated together.")


try:
    print(y/0)
except ZeroDivisionError:
    raise Exception("Any number cannot be divided by 0")


try: 
    print(i)
except AssertionError:
    raise Exception("The variable cannote be accessed as it's not present") 
