# mode selection recomendation >3km walk 3-15 bike else car
distance=int(input("how much distance:"))

if (distance<=3):
    mode="walk"
elif (distance<=15):
    mode="bike"
else:
    mode="car"

print("i suggest to choose",mode)