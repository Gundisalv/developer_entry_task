
from developer_entry_task.functions.functions import DeveloperEntryTask


a = DeveloperEntryTask()
print(a.get_statistics(42))
print(a.get_statistics('forest'))
print(a.get_closest_pair([2 , 3 , 5 , 7 , 11],'min'))
print(a.get_closest_pair(list(range(10**4)),'mean', 'std'))

