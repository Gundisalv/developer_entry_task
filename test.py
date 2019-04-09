from developer_entry_task.functions.functions import DeveloperEntryTask


Developer_Entry_Task = DeveloperEntryTask()

Developer_Entry_Task.get_statistics(42)

Developer_Entry_Task.get_statistics('forest')

Developer_Entry_Task.get_closest_pair([2 , 3 , 5 , 7 , 11],'min')

Developer_Entry_Task.get_closest_pair(list(range(10**4)),'mean', 'std')