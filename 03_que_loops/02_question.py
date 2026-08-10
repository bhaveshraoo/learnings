# sum,count of even number upto n
n = int(input("upto?"))
sum_even = 0
for i in range(1, n+1):
    if i % 2 == 0:
        sum_even += i

print("answer", sum_even)
