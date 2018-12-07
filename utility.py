# coding=utf-8
# 

import os, configparser



def get_current_path():
	"""
	Get the absolute path to the directory where this module is in.

	This piece of code comes from:

	http://stackoverflow.com/questions/3430372/how-to-get-full-path-of-current-files-directory-in-python
	"""
	return os.path.dirname(os.path.abspath(__file__))



def _load_config(config_file='web.config'):
	"""
	Read the config file, convert it to a config object.
	"""
	cfg = configparser.ConfigParser()
	cfg.read(config_file)
	return cfg



# initialized only once when this module is first imported by others
if not 'config' in globals():
	config = _load_config()



def get_backup_directory():
	"""
	The directory where the backup files reside.
	"""
	global config
	return config['backup']['directory']



def get_n_days():
	global config
	return int(config['clear']['days'])



def get_remote_host():
	global config
	return config['webserver']['host']



def get_user():
	global config
	return config['webserver']['user']



def get_password():
	global config
	return config['webserver']['password']
