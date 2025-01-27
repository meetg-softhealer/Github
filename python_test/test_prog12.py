
def bracketMatcher(x):
    open_ctr = 0
    close_ctr = 0

    for i in x:
        if "(" in i:
            open_ctr = open_ctr + 1
        elif ")" in i:
            close_ctr = close_ctr + 1
        else: 
            pass

    if open_ctr != close_ctr:
        return 0
    else:
        return 1

x = "(hello)(world))"
print(bracketMatcher(x))

