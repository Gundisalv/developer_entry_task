from developer_entry_task.functions.functions import DeveloperEntryTask


Developer_Entry_Task = DeveloperEntryTask()

result = Developer_Entry_Task.get_statistics(42)
print(result)
result = Developer_Entry_Task.get_statistics('forest')
print(result)
result = Developer_Entry_Task.get_closest_pair([2 , 3 , 5 , 7 , 11],'min')
print(result)
result = Developer_Entry_Task.get_closest_pair(list(range(10**4)),'mean', 'std')
print(result)