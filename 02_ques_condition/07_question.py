# coffee small medium or large and extra shot yes or no
size=str(input("size:"))
extra= (input("extra short? ")) == "yes"

if extra:
    coffee = size + "with extra shot"
else:
    coffee = size + "simple"

print("pls confirm:",coffee)
