import datetime

current = datetime.datetime.now()
temp1 = datetime.datetime.now()
year = current.year
month = current.month
day = current.day
date_from_txt = input()

print(current)
#current = current - datetime.timedelta(days = 1)
print(current)
flag =0
if date_from_txt == str(year)+'.'+str(month)+'.'+str(day) :
    flag = 1
print(flag)
print(date_from_txt)
print(year)
print(month)
print(day)
