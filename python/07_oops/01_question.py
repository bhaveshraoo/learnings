# basic class and object , create a car class with attributes like brand, model. then create an isntance of this class 
class Car:
    total_cars=0 
    # line8
    def __init__(self, ubrand, umodel):
        self.__brand=ubrand
        self.__model=umodel
        Car.total_cars +=1
     
    def get_brand(self):
        return self.__brand + "!"
    def fuel_type(self):
        return "petrol or deisel "

# add fuctionality that can type name together
    def full_name(self):
        return f"{self.__brand}{self.__model}{self.fuel_type()}"
    
#Static Method:Add a static method to the Car class that returns a general description of a car    
    @staticmethod
    def general_description():
        return "car is car "
    
# Property Decorators: Use a property decorator in the Car class to make the model attribute read-only.
    @property
    def get_model(self):
        return self.__model + "!"
    

# inharitance add a new class electric_car that inherit from car and extra atribute battry_size
class Electric_car(Car):
    def __init__(self, brand, model, battry_size):
        super().__init__(brand, model)
        self.battry_size=battry_size
    def fuel_type(self):
        return "electric charge "
    
# Class Inheritance and isinstancel Function: Demonstrate the use of isinstance to check if my_tesla is an instance of Car and ElectricCar.


# encapsulation modify the car class to encapsulate the brand attribute, make it private, provide a getter method for it

 # if we have to privatise any object we are still using
 # brand but now we change it to __brand its now private cant be access directly only by a def function
 # line4
        
# polymorphism : Demonstrate polymorphism by defining a method fuel_type in both Car and ElectricCar classes, but with different behaviors.
 # line 10 and 25


# class variable add a class variable to car data, keep the track of the number of car created
 # line 3 & 8




my_tesla= Electric_car("tesla", " s1", " 30kWh")
my_car= Car("toyota ", "innova ")

my_new_car = Car("tata", "safari")


# print(isinstance(my_car, Car))
# print(isinstance(my_car, Electric_car))
    

Car("Tataaa", "safariii")
# print(my_car.brand)
# print(my_car.full_name())



# print(my_new_car.get_model)

# print(my_tesla.brand)
# print(my_tesla.fuel_type())

# print(Car.total_cars)
# print(my_new_car.general_description())
# print(Car.general_description())

# question :Multiple Inheritance
# Problem: Create two classes Battery and Engine, and let the ElectricCar class inherit from both, demonstrating multiple inheritance.

class battry:
    def battry_info(self):
        return "battryyyyyyy"

class engine:
    def engine_info(self):
        return"engineeee"
    

class Electricar2(battry, engine, Car):
    pass

my_new_tesla=Electricar2("BYD", "s2")

print(my_new_tesla.battry_info())
print(my_new_tesla.engine_info())
print(isinstance(my_new_tesla, Car))
