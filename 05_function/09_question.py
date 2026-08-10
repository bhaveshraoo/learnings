#  generate a function with yield || write a generator function that yield even number up to limit
def even_generator(limit):
    for i in range(2, limit+1, 2):
        yield(i)


for num in even_generator(10):
    print(num)