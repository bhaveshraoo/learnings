# age grp classifiyer child((0-12), teen(13-19), adult(20-60), senior(60+))
age=int(input("whats your age:"))
if (age<=12):
    print("child")
elif (age<20):
    print("teen")    
elif (age<60):
    print("adult") 
else:
    print("budhe")   
