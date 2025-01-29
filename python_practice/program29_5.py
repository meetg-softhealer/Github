import calendar

y = int(input("Enter Year:"))
m = input("Enter month:")

m = m.lower()


mon = ['january','february','march','april','may','june','july','august','september','october','november','december']

for i in range(len(mon)):
    if m==mon[i]:   
        print(calendar.month(y,i+1))
        
        


        




