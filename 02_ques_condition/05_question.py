# sugeest activity based on weather sunny walk , rainy read book , snowy make snowman
weather=str(input("whats the weather:"))

if (weather=="rainy"):
    activity= "read book"
elif(weather=="sunny"):
    activity="walk"
elif(weather=="snowy"):
    activity="make a snowman"
else:
    print("wrong input")
    exit()
    
print("i suggest you according to weather u have to",activity)        
