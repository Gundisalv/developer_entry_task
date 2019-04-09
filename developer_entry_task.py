import datetime
from developer_entry_task.functions.functions import DeveloperEntryTask

if __name__ == "__main__":
    t0 = datetime.datetime.now() 
    print('Running test values for all functions')
    print('Pre-processing inputs')
    Developer_Entry_Task = DeveloperEntryTask()
    print('Runing first test. Get statistics of a polygon ID. ' 
        'get_statistics(42)')
    print('Result', Developer_Entry_Task.get_statistics(42))
    print('Runing second test. Get statistics of a class name. '
        'get_statistics(\'forest\')')
    print('Result', Developer_Entry_Task.get_statistics('forest'))
    print('Runing third test. Get closest pair for one criteria. '
        'Developer_Entry_Task.get_closest_pair('
        '[2 , 3 , 5 , 7 , 11],\'min\')')
    print('Result', Developer_Entry_Task.get_closest_pair(
        [2 , 3 , 5 , 7 , 11],'min'))
    print('Runing forth test. Get closest pair for one criteria. '
        'Developer_Entry_Task.get_closest_pair(list(range(10**4)),'
        '\'mean\', \'std\')')
    print('Result', Developer_Entry_Task.get_closest_pair(list(range(10**4)),'mean', 'std'))
    print('Elapsed time:', datetime.datetime.now() - t0)
   