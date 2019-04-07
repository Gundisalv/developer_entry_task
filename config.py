import os
import sys

basedir = os.path.abspath(os.path.dirname(__file__))

if os.path.exists('config.env'):
    print('Importing environment from .env file')
    for line in open('config.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")

if not os.path.exists('./shub_downloads'):
    os.mkdir('shub_downloads')

class Config:
    SENTINEL_INSTANCE_ID = os.environ.get('SENTINEL_HUB_ID') or False
    if not SENTINEL_INSTANCE_ID:
        print('SENTINEL_HUB_ID needed to continue')
        exit(0)