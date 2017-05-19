import io
import os
import re
import sys
import json
import subprocess
import requests
import json
import config
import logging
from github import Github
from flask import Flask, request, abort, jsonify
from extract import Extract
from predict import Predict


app = Flask(__name__)
logging.basicConfig(filename='src/logs/emma.log',level=logging.DEBUG)

@app.route("/payload", methods=["POST"])
def payload():
    json_payload = json.loads(request.form['payload'])

    if json_payload['action'] != 'opened':
        extr = Extract()
        # to be used 
        # pr_diff_url = json_payload['pull_request']['diff_url']
        parsed_diff = extr.get_pr_diff('https://patch-diff.githubusercontent.com/raw/facebook/react/pull/3.diff')
        # parsed_diff = extr.get_pr_diff(pr_diff_url)

        predictions = []
        prdt = Predict()
        
        for diff in parsed_diff:
            # print(diff)
            deleted_lines = diff['deleted_lines']
            added_lines = diff['added_lines']
            file_name = diff['file_name']
            # timestamp = json_payload['created_at']
            timestamp = '2017-04-20T23:37:53+0518'

            for deleted_line in deleted_lines:
                test_dict = {
                    'file': file_name,
                    'line': deleted_line,
                    'timestamp': timestamp
                }
                predictions.append([prdt.train(test_dict)])

        print('Predictions !!!')
        print(predictions)

        logging.info('Prediction' + str(predictions))

        credentials = config.read_credentials()
        repo_details = config.read_repo()

        g = Github(credentials.username, credentials.password)
        org = g.get_organization(repo_details.org)
        repo = org.get_repo(repo_details.repo)

        issue = repo.get_issue(1)
        # pr = repo.get_pull(1)
        # pr.create_comment()
        issue.create_comment('Hi, thanks for the PR, according to the analysis I\'ve found out that :tada:' + str(predictions))

        return app.response_class(['POSTED', 'PR/ISSUE'], content_type='application/json')

if __name__ == "__main__":
    try:
        port_number = int(sys.argv[1])
    except ValueError:
        port_number = 80
    host = os.environ.get('HOST', '0.0.0.0')
    is_dev = os.environ["DEV"]
    if host == '0.0.0.0':
        host = '127.0.0.1'
    app.run(host=host, port=port_number, debug=is_dev)
