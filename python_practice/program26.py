dict1 = {'a':1,'b':2,'c':3}
dict2 = {'d':4,'e':5,'f':6}


def add_dict(d1,d2):
    d3 = {}
    d3.update(d1)
    d3.update(d2)
    print(d3)

add_dict(dict1,dict2)
