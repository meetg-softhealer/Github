str1 = "Hello321Bye360"

nums  = "0123456789"
Digit = 0
Letter = 0
for i in str1:
    if i in nums:
        Digit = Digit + 1
    else:
        Letter = Letter + 1

print(Digit)
print(Letter)