# **kwargs create a internet, accept any number of the keyword argument and print them in the format of key: value**
def print_kwargs(**kwargs):
    for key, value in kwargs.items():
        print (f"{key}: {value}")


print_kwargs(name="khoti", power="kamchor")
print_kwargs(name="sanu", power="ladai", kam="thali")
print_kwargs(name="bhavesh")
