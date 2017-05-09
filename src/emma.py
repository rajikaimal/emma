import io
import os
import re
import sys
import json
import subprocess
import requests
from flask import Flask, request, abort
from extract import Extract
from predict import Predict


app = Flask(__name__)

@app.route("/payload", methods=["POST"])
def payload():
    print(request.json)
    exrt = Extract()
    prdt = Predict()

    ex.get_parsed_diff('/home/rajika/projects/prepack')
    prdt.train([{'file': 'src', 'line': '8', 'timestamp': '2017-04-24T17:07:51-0700'}])
    
    return app.response_class(['Ok', 'Fine'], content_type='application/json')


# @app.route("/test", methods=["GET"])
# def test():
#     parse = Parse()
#     diff = parse.parse_diff_file("/data/001.diff")
#     return app.response_class(json.dumps(diff), content_type='application/json')

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
