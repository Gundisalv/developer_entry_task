import os
from log import get_logger

logger = get_logger(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

if os.path.exists('config.env'):
    logger.info('Importing environment variables')
    for line in open('config.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")
else:
    logger.error('Missing environment variables file')
    exit(0)

if not os.path.exists('./shub_downloads'):
    os.mkdir('shub_downloads')

class Config:
    SENTINEL_INSTANCE_ID = os.environ.get('SENTINEL_HUB_ID') or False
    if not SENTINEL_INSTANCE_ID:
        logger.error('SENTINEL_HUB_ID needed to continue')
        exit(0)
    RESAMPLE_VAL = 1000000000