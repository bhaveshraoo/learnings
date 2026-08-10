# pass checker
password=str(input("ur pass: "))
count=len(password)

if(count<6):
    strength="weak"
elif(count<10):
    strength="avg"
else:
    strength="good"

print("ur pass is",strength)
