from logging.handlers import TimedRotatingFileHandler
import logging
import sys
import os

if not os.path.exists('logs'):
    os.mkdir('logs')

if not os.path.exists('logs/developer_entry_task.log'):
    open("logs/developer_entry_task.log", "w+").close()

formater = logging.Formatter(
    '[%(levelname)s] - %(name)s - %(asctime)s - %(message)s')
file_handler = TimedRotatingFileHandler('logs/developer_entry_task.log',
                                        when='midnight', backupCount=20)
file_handler.setFormatter(formater)
file_handler.suffix = "%Y-%m-%d"


def get_logger(name):
    log = logging.getLogger(name)
    if '--debug' not in sys.argv:
        log.setLevel(logging.INFO)
    else:
        log.setLevel(logging.DEBUG)
    log.addHandler(file_handler)
    return log
