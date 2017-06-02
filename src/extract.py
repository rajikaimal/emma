import requests
import os
import csv
from github import Github
from git import Repo
from parser import Parser

class Extract:
	"""
	Extract data from .git repo and persist as a data set
	"""
	# repos name git: .git
	# destination absolute path
	def clone_repo(self, repo_name, destination):
		Repo.clone_from(repo_name, destination)
		print('Cloning complete ...')

	# get parsed .diff file
	def get_parsed_diff(self, repo_path):
		prev_commiter = None
		parser = Parser()
		full_path = os.path.dirname(
            os.path.realpath(__file__))
		for diff_info in parser.parse_diff(repo_path):
			# print(diff_info)
			if not 'file_name' in diff_info:
				print('Nope !')
				continue
			with open(full_path + '/data/train_emma.csv', 'a') as csv_file:
				writer = csv.writer(csv_file)
			    # for key, value in diff_info.items():
			    #    if(key == 'file_name'):
			    #    		for file_name in value:
			    #    			# print('writing')
				
				if(prev_commiter == None):
					writer.writerow([diff_info['file_name'], diff_info['lines'], diff_info['timestamp'], diff_info['author'], diff_info['author']])
				else:
					writer.writerow([diff_info['file_name'], diff_info['lines'], diff_info['timestamp'], diff_info['author'], prev_commiter])

				prev_commiter = diff_info['author']
	
	def get_pr_diff(self, pr_diff_url):
		if pr_diff_url:
			r = requests.get(pr_diff_url)
			raw_diff = r.content.decode("utf-8")
			parser = Parser()
			parser = Parser()
			parsed_diff = parser.parse_raw_diff(raw_diff)
			# print(parsed_diff)
			return parsed_diff
			# parsed_diff = parser.parse_raw_diff(str(raw_diff))
			# 	print(parsed_diff)

# ex = Extract()
# ex.clone_repo("https://github.com/claireorg/sample", "/home/rajika/Desktop/test")
# exxx = ex.get_parsed_diff('/home/rajika/projects/sample')
# # print(exxx)
# parsed_diff = ex.get_pr_diff('https://patch-diff.githubusercontent.com/raw/facebook/react/pull/3.diff')
# # print(parsed_diff)
