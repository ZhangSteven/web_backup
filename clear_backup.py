# coding=utf-8
# 
# Clear the backup files that are too old.

from utils.file import getFiles
from web_backup.utility import get_backup_directory, get_n_days
from os.path import getmtime, join
from datetime import datetime, timedelta
import logging
logger = logging.getLogger(__name__)



def olderThanNdays(fn, nDays=get_n_days()):
    """
    [String] fn => [Bool] file date older than N days
    """
    dateString = lambda fn: fn[3:11] if fn.startswith('db') else fn[4:12]
    fnToDate = lambda fn: datetime.strptime(dateString(fn), '%m-%d-%y')

    return datetime.now() - fnToDate(fn) > timedelta(days=nDays)



def toFullPath(fn):
    """
    [String] fn => [String] full path fn
    """
    return join(get_backup_directory(), fn)



if __name__ == '__main__':
    import logging.config, os
    logging.config.fileConfig('logging.config',                
            disable_existing_loggers=False)
	
    logger.info('Start clearing')

    """
    for fn in filter(olderThanNdays, 
		map(toFullPath, getFiles(get_backup_directory()))):
        try:
            os.remove(fn)
            logger.debug('removed {0}'.format(fn))
        except:
            logger.exception()
    """

    for fn in map(toFullPath
                 , filter(olderThanNdays
                         , getFiles(get_backup_directory()))):
        try:
            print('deleting {0}'.format(fn))
            os.remove(fn)
        except:
            logger.exception()
