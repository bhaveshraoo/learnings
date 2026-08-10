# find the first non repeat character
input_str="teeters"
for char in input_str:
   if input_str.count(char)==1:
       
     print(char)
     break