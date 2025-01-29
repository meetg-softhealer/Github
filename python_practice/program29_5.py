import calendar
from datetime import datetime

y = int(input("Enter Year:"))
m = input("Enter month:")

m = m.lower()
mon = datetime.strptime(m,"%B").month
print(calendar.month(y,mon))
      
        
        


        




