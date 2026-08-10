# check all the elements of the list are unique if same then exit loop
items=["apple", "banana", "orange", "apple", "mango"]

unique_item= set()
for item in items:

 if item in unique_item:
    print("duplicate",item)
    break
 unique_item.add(item)
 print(item)