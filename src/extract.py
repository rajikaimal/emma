import os
import csv
from parser import Parser

class Extract:
	"""
	Extract data from .git repo and persist as a data set
	"""
	# repos name git: .git
	# destination absolute path
	def clone_repo(self, repo_name, destination):
		Repo.clone_from(repo_name, destination)

	# get parsed .diff file
	def get_parsed_diff(self, repo_path):
		prev_commiter = None
		parser = Parser()
		full_path = os.path.dirname(
            os.path.realpath(__file__))
		for diff_info in parser.parse_diff(repo_path):
			print(diff_info)
			with open(full_path + '/data/train_emma.csv', 'a') as csv_file:
			    writer = csv.writer(csv_file)
			    for key, value in diff_info.items():
			       if(key == 'file_names'):
			       		for file_name in value:
			       			print('writing')
			       			if(prev_commiter == None):
				       			writer.writerow([file_name, diff_info['lines'], diff_info['timestamp'], diff_info['author'], diff_info['author']])
				       		else:
				       			writer.writerow([file_name, diff_info['lines'], diff_info['timestamp'], diff_info['author'], prev_commiter])

			       			prev_commiter = diff_info['author']

ex = Extract()
ex.get_parsed_diff('/home/rajika/projects/babel-bot')