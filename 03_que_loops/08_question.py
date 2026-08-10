#  prime number checker
n=int(input("enter"))
# num=True
if n>0 :
 for i in range(2,n):
  if (n%i)==0:
   print("not prime")
   break
  else:
   print("yes prime")
   break