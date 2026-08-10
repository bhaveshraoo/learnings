# # function that return both area and circumference at same time by radius
# def area(r):
#     return(2*3.14*r)

# def circum(r):
#     return(3.14*(r**2))

# print(("area",area(3),("circum",circum(3))))

import math
def circle(radius):
    area=math.pi*radius**2
    circum=(2*math.pi*radius)
    return area, circum

a,c=circle(3)
print("area:",a , "circum",c)


