import configparser
import os

Config = configparser.ConfigParser()
full_path = os.path.dirname(os.path.realpath(__file__))

def read_credentials():
	Config.read(full_path + '/config/config_details.ini')
	try:
		username = Config['Credentials']['username']
		password = Config['Credentials']['password']
		return {
			'username': username,
			'password': password
		}
	except ValueError:
		print('Error !')

def read_repo():
	Config.read(full_path + '/config/config_details.ini')
	try:
		org = Config['Repository']['org']
		repo = Config['Repository']['repo']
		return {
			'org': org,
			'repo': repo
		}
	except ValueError:
		print('Error !')
