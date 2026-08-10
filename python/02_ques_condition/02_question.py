# movie ticket selling child=8rs adlut(18-60)=12rs everyine 2rs discount on wednesday
age=int(input("ur age:"))
day=str(input("day:"))

price = 12 if age >=18 else 8

if day=='wednesday':
  price=price-2 
#   also write as price-=2
print("your ticket price is:", price)
