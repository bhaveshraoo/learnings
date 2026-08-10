#  *args create a function that take variable number of argument and return their SUM
def sum_all(*args):
    print(args)
    return sum(args)

print((sum_all(2, 2, 9)))
print((sum_all(2, 2, 9, 7)))
print((sum_all(2, 2, 9, 7, 0, 5)))
print((sum_all(2, 2, 9, 7, 0, 5, 4)))