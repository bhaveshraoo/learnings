fruit_name=str(input("whats fruit:"))

if (fruit_name=="banana"):
    color=str(input("whats color of fruit:"))
    if (color=="green"):
        fruit="unripe"
    elif(color=="yellow"):
        fruit="ripe"   
    elif(color=="brown"):
        fruit="overripe"
    
    print("fruit:",fruit)
else:
    print("fruit is not available")