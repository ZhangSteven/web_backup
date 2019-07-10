#!/usr/bin/env python3
#
# coding=utf-8
# 
# Copy the backup files over from the production web server
#
# This is to help the backup web server to copy backup data from the
# production server.

from utils.file import getFiles
from utils.mail import sendMail
from web_backup.utility import get_backup_directory, get_user, \
        get_password, get_remote_host, get_current_path, \
        getMailSender, getMailRecipients, getMailServer, \
        getMailTimeout
from web_backup.clear_backup import toFullPath
from os.path import join
from subprocess import call
from datetime import timedelta, datetime
from itertools import chain
from functools import reduce
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
    #print(command)
    return call(command)



def doCopy():
    """
    ([List] successful files, [List] failed files)

    Copy backup files from the remote machine (production web server),
    then return the copy status as two lists.
    """
    result = lambda fn: (fn, copyFromRemoteHost(fn))
    def build(acc, el):
        success, failure = acc
        fn, status = el
        if (status == 0):
            logger.info('doCopy(): copied {0}'.format(fn))
            return (success + [fn], failure)
        else:
            logger.error('doCopy(): failed to copy {0}'.format(fn))
            return (success, failure + [fn])

    return reduce(build
                 , map(result
                      , map(toFullPath, backupLast7days()))
                 , ([], []))



def deliverResult(success, failure):
    """
    [List] success, [List] failure => send email notification about the
    status.
    """
    logger.debug('sendMail(): {0}, {1}'.format(success, failure))
    list2string = lambda title, L: '{0}: {1} file(s)'.format(title, len(L)) \
                                   + '\n' \
                                   + '\n'.join(L)
    body = lambda success, failure: list2string('success', success) \
                                    + '\n\n' \
                                    + list2string('failure', failure)

    good = 'Web server backup copy result'
    bad = 'Error occurred during web server backup copy process'
    subject = lambda success, failture: bad if len(success) == 0 or \
                                                len(failure) > 0 \
                                            else good

    sendMail(body(success, failure)
            , subject(success, failure)
            , getMailSender()
            , getMailRecipients()
            , getMailServer()
            , getMailTimeout())



if __name__ == '__main__':
    import logging.config
    from os.path import join
    logging.config.fileConfig(join(get_current_path(), 'logging.config')
                             , disable_existing_loggers=False)
	
    logger.info('Start copy over')
    deliverResult(*doCopy()) # unpack the result of doCopy(), then pass to
                             # deliver result
