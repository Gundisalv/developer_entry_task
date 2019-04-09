# Answers for the Sinergise python developer entry task

This code will give answers to the problems presented on the Python Developer 
Entry Task manual.

I have decided to nucleate the main functions within a class so preprocessing of
data has to be done just once and several tests can be run.


## Getting Started

These instructions will get you a copy of the project up and running on your 
local machine for development and testing purposes.


### Prerequisites

This program was built using Python 3.7.1 you would need it to be installed on 
your computer before we start.

Be sure to also install the python-dev libraries and pip.


### Installing

To run the program we will need the libraries that are listed on requirements.txt 
to install them do


```
pip install -r requirements.txt
```

## Set config.env

Config env example:

    [DEFAULT]
    SENTINEL_HUB_ID=INSET_ID_HERE



## Running

To run the full program just write


```
python developer_entry_task.py
```


it will print some selected examples for each of the functions required on the 
test, with it respective execution time. Al functions have been optimized,
but I still can not manage to get the full execution under one minute.

### Run by function

To run specific tests for each function you must import the class 
DeveloperEntryTask into your own code or use the included test.py file.

```
python test.py
```
## Authors

*   Gonzalo Quiroga - _Initial work_ - [Gundisalv](https://github.com/Gundisalv)

## Acknowledgments

*   Hat tip to anyone whose code was used.
*   Friends.
*   The internet.
