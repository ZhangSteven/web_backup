# coding=utf-8
# 
# Copy the backup files over from the production web server
#
# This is to help the backup web server to copy backup data from the
# production server.

from utils.file import getFiles
from web_backup.utility import get_backup_directory, get_user, \
        get_password, get_remote_host
from web_backup.clear_backup import toFullPath
from os.path import join
from subprocess import call
from datetime import timedelta, datetime
from itertools import chain
import logging
logger = logging.getLogger(__name__)



def backupLast7days():
	"""
	[List] file names of backup files generated in the last 7 days.

	The main web server generates backup files every Tuesday and Friday,
	with the below naming convention:

	web-mm-dd-yy.tar.gz
	db-mm-dd-yy.sql.gz
	"""
	dateString = lambda d: d.strftime('%m-%d-%y')
	tuesOrThurs = lambda d: True if d.weekday() in [1, 4] else False
	pastDate = lambda days: datetime.now() - timedelta(days=days)	
	webFile = lambda dstring: 'web-' + dstring + '.tar.gz'
	dbFile = lambda dstring: 'db-' + dstring + '.sql.gz'
	
	dateStrings = list(map(dateString
				   	 	  , filter(tuesOrThurs
						   	 	  , map(pastDate, range(1, 8)))))

	return chain(map(webFile, dateStrings), map(dbFile, dateStrings))



def copyFromRemoteHost(fn):
    """
    [String] fn => [int] return code of executing the command

    Call the sshpass command to invoke a scp process to copy the files
	from the remote machine.
    """
    command = ['sshpass', '-p', '{0}'.format(get_password()), 'scp',
		'{0}@{1}:{2}'.format(get_user(), get_remote_host(), fn),
        get_backup_directory()	
		]
    print(command)
    return call(command)



if __name__ == '__main__':
    import logging.config
    logging.config.fileConfig('logging.config',   
                                disable_existing_loggers=False)
	
    logger.info('Start copy over')
    for fn in map(toFullPath, backupLast7days()):
        if (copyFromRemoteHost(fn) == 0):
            print('copied {0}'.format(fn))
        else:
            print('failed to copy {0}'.format(fn))

        
