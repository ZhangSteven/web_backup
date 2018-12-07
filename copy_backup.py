# coding=utf-8
# 
# Copy the backup files over from the production web server

from utils.file import getFiles
from web_backup.utility import get_backup_directory, get_user, get_password, \
								get_remote_host
from web_backup.clear_backup import olderThanNdays, toFullPath
from os.path import join
from subprocess import call
import logging
logger = logging.getLogger(__name__)



def get_file_list(fn):
	"""
	[String] fn => [List] file names

	fn : the file containing the list files copied before
	"""
	with open(fn) as f:
		return [line.rstrip('\n') for line in f]



def withinAweek(fn):
	"""
	[String] fn => [Bool] file last modified date within one week
	"""
	return not olderThanNdays(fn, 7)



def copyToRemoteHost(fn):
	"""
	[String] fn => [int] return code of executing the command

	Call the sshpass command to invoke a scp process to copy the file over
	"""
	command = ['sshpass', '-p', '{0}'.format(get_password()), 'scp', fn,
				'{0}@{1}:{2}'.format(get_user(), get_remote_host(), get_backup_directory())
		]
	print(command)
	return call(command)



if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('logging.config', disable_existing_loggers=False)
	
	logger.info('Start copy over')
	for fn in filter(withinAweek, 
				map(toFullPath, getFiles(get_backup_directory()))):
	
		if copyToRemoteHost(fn) == 0:
			logger.debug('copied {0}'.format(fn))
		else:
			logger.error('failed to copy {0}'.format(fn))
			

