# grade calculator a(90-100), b(80-89), c(70-79), d(60-69), f(0-60))
mark=int(input("ur marks:"))
if mark>=101 :
    print("aukat me")
    exit()

# if(mark>=90):
#     print("ur grade is:A")

# elif(mark>=80):
#     print("ur grade is:B")    

# elif(mark>=70):
#     print("ur grade is:c")    

# elif(mark>=60):
#     print("ur grade is:d")    

# else:
#     print("ur grade is:f")  

# 2nd way
if(mark>=90):
    grade="A"

elif(mark>=80):
    grade="B"

elif(mark>=70):
    grade="C"

elif(mark>=60):
    grade="D"
    
else:
    grade="F"

    print("ur grade is",grade)