from django.test import TestCase

# Create your tests here.
import datetime
timestring = "326:0:0"
my_worktime = "500:30:25"

worktime = timestring.split(':')
work_hours = int(worktime[0])
work_minutes = int(worktime[1])
work_seconds = int(worktime[2])

new_time = datetime.timedelta(hours=work_hours, minutes=work_minutes, seconds=work_seconds)
my_time = datetime.timedelta(hours=int(my_worktime.split(':')[0]), minutes=int(my_worktime.split(':')[1]), seconds=int(my_worktime.split(':')[2]))

my_worktime = my_time + new_time
print(my_worktime)
hours, remainder = divmod(my_worktime.seconds + my_worktime.days * 24 * 3600, 3600)
minutes, seconds = divmod(remainder, 60)
my_worktime = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
print(my_worktime)
