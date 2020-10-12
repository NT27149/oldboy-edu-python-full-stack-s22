import os
import logging.config
from conf.setting import LOG_PATH


standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s]' \
                  '[%(filename)s:%(lineno)d][%(levelname)s][%(message)s]'

logfile_path = os.path.join(LOG_PATH, 'manager.log')

LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        }
    },
    'filters': {},
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': logfile_path,
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
    },
}


def create_logging(name, info):
    logging.config.dictConfig(LOGGING_DIC)
    logger = logging.getLogger(name)
    logger.debug(info)
