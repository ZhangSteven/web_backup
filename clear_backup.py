# coding=utf-8
# 
# Clear the backup files that are too old.

from utils.file import getFiles
from web_backup.utility import get_backup_directory, get_n_days
from os.path import getmtime, join
import datetime
import logging
logger = logging.getLogger(__name__)



def olderThanNdays(fn, nDays=get_n_days()):
	"""
	[String] fn => [Bool] file last modified date larger than N days
	"""
	return datetime.datetime.now() - datetime.datetime.fromtimestamp(getmtime(fn)) > datetime.timedelta(days=nDays)



def toFullPath(fn):
	"""
	[String] fn => [String] full path fn
	"""
	return join(get_backup_directory(), fn)



if __name__ == '__main__':
	import logging.config, os
	logging.config.fileConfig('logging.config', disable_existing_loggers=False)
	
	logger.info('Start clearing')
	for fn in filter(olderThanNdays, 
				map(toFullPath, getFiles(get_backup_directory()))):

		try:
			os.remove(fn)
			logger.debug('removed {0}'.format(fn))
		except:
			logger.exception()
			

