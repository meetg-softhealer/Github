str1 = "What is Lorem Ip sum Lorem Ipsum is simply dummy text of the printing and typesetting industry Lorem Ipsum has been the industry's standard dummy text ever since the 1500s when an unknown printer took a galley Of type and scrambled it to make a type specimen book it has?"

str1 = str1.lower()

dict1 = {"a": 0,
         "e": 0,
         "i": 0,
         "o": 0,
         "u": 0
        }

for x in str1:
    if x=="a" or x=="e" or x=="i" or x=="o" or x=="u":
        dict1[x] = dict1[x] + 1 

print(dict1)