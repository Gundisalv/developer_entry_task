
from developer_entry_task.functions.functions import DeveloperEntryTask
import datetime

t0 = datetime.datetime.now()
a = DeveloperEntryTask()
a1 = datetime.datetime.now() - t0
print(a1)
print(a.get_statistics(42))
a2 = datetime.datetime.now() - t0
print(a2-a1)
print(a.get_statistics('forest'))
a3 = datetime.datetime.now() - t0
print(a3-a2)
print(a.get_closest_pair([2 , 3 , 5 , 7 , 11],'min'))
a4 = datetime.datetime.now() - t0
print(a4-a3)
print(a.get_closest_pair(list(range(10**4)),'mean', 'std'))
a5 = datetime.datetime.now() - t0
print(a5-a4)
