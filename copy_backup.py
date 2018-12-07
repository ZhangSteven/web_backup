# coding=utf-8
# 
# Copy the backup files over from the production web server

from utils.file import getFiles
from web_backup.utility import get_backup_directory
import logging
logger = logging.getLogger(__name__)



fileList = get_file_list(get_copy_file())

def get_file_list(fn):
	"""
	[String] fn => [List] file names

	fn : the file containing the list files copied before
	"""
	with open(fn) as f:
		return [line.rstrip('\n') for line in f]



def notCopiedBefore(fn):
	"""
	[String] fn => [Bool] file not in the "copy file", i.e., not copied before
	"""
	global fileList
	return not (fn in fileList)



def toFullPath(fn):
	"""
	[String] fn => [String] full path fn
	"""
	return join(get_backup_directory(), fn)



do copyToRemoteServer(fn):
	pass



if __name__ == '__main__':
	import logging.config, os
	logging.config.fileConfig('logging.config', disable_existing_loggers=False)
	
	logger.info('Start copy over')
	nFile = 0
	for fn in filter(olderThanNdays, 
				map(toFullPath, getFiles('/my_stuff/backup'))):

		try:
			os.remove(fn)
			logger.debug('removed {0}'.format(fn))
		except:
			logger.exception()
			

