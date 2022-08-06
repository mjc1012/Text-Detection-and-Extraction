from datetime import datetime

date_time_str = '10-08-2021 07:52 AM'

date_time_obj = datetime.strptime(date_time_str, '%d-%m-%Y %H:%M %p')


print ("The type of the date is now",  type(date_time_obj))
print ("The date is", date_time_obj)