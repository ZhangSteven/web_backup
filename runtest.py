#!/usr/bin/env python3
#
# coding=utf-8
# 
# Test how to run a python script directly from command line.
#

from web_backup.utility import get_current_path
import logging
logger = logging.getLogger(__name__)



if __name__ == '__main__':
    import logging.config
    """
    Note: if we want to the python script like:

    /home/cuser/git/web_backup/runtest.py

    Then it won't work because

    1. Load the logging config file is relative to local directory
    2. Path to log files (check the logging.config) is relative to 
        local directory.

    To make it work, we need to wrap it into a runtest.sh file, with
    two lines inside:

        cd /home/cuser/git/web_backup/
        ./runtest.py

    Check out /my_stuff/scripts/copy_back.sh
    """
    from os.path import join
    logging.config.fileConfig(join(get_current_path(), 'logging.config')
                             , disable_existing_loggers=False)
    print('run test')
    logger.info('Start copy over')

