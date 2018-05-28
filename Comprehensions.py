# simple list comprehensions example
ls = [n for n in range(11)]
print ls

# list comprehensions for n*n
ls = [n * n for n in range(11)]
print ls

# list comprehensions for even n
ls = [n for n in range(11) if n % 2 != 1]
print ls

# map(), filter()

#dict comprehensions
OSs = ['Android', 'OSX', 'Windows']
Vendors = ['Google', 'Apple', 'Microsoft']
HW = ['smartphone', 'Mac', 'PC']
ls = {vendor:os for vendor,os in zip(Vendors, OSs)}
print ls

# set comprehensions
my_set = [1,1,2,6,7,5,4,8,7,6,3,2,8]
my_set = {n for n in my_set}
print my_set
