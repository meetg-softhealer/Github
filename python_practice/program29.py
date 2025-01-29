from datetime import datetime

x = {}
for i in range(3):
    k = str(input(f"Enter the Name {i+1}:")) 
    v = str(input(f"Enter the date {i+1}:"))
    x[k] = v

y = {}
for i in x.keys():
    y[i] = datetime.strptime(x[i], "%d-%m-%Y")
    
low_date = max(y.values())
high_date = min(y.values())

for k,v in y.items():
    if v==high_date:
        print(f"{k} is older")
    elif v==low_date:
        print(f"{k} is younger")
    

    


