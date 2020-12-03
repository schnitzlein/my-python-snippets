# https://www.programiz.com/python-programming/datetime

# Testdata: 'Sun 10 May 2015 13:54:36 -0700'

from datetime import datetime

#datetime(year, month, day)
a = datetime(2018, 11, 28)
print(a)

#TODO: parse Month string in number
# datetime(year, month, day, hour, minute, second, microsecond)
b = datetime(2015, 5, 10, 13, 54, 36, 342380)
print(b)