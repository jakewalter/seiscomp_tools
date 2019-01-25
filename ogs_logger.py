"""
Filename: ogs_logger.py
Purpose: Setup the logger used by earthquake script.
Author: Bill Greenwood
Date: 20170115
"""

import logging
import logging.handlers

LOG_FORMAT = '%(levelname)s %(asctime)s %(filename)s ' \
             'Function: %(funcName)s Line #: %(lineno)d %(message)s'

def set_logger(filename, log_level=logging.WARNING):
    """
    Function to create the logger.  A log file will not be created until
        actually needed. When the size get to 5MB the file will be
        rotated with 14 backups kept.

    Arguments:
    @param {str} filename - full path and filename of the logfile
    @param {int} log_level (30 or legging.WARNING) - logging level
    @return logger - The logger object.
    """
    logger = logging.getLogger("earthquake")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    file_handler = logging.handlers.RotatingFileHandler(filename,
                                                        maxBytes=5242880,
                                                        backupCount=14,
                                                        delay=False)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
