import io
import os
import re
import sys
import json
import subprocess
import requests
import ipaddress
from flask import Flask, request, abort

app = Flask(__name__)

@app.route("/payload", methods=["POST"])
def payload():
    print(request.json)

if __name__ == "__main__":
    try:
        port_number = int(sys.argv[1])
    except ValueError:
        port_number = 80
    host = os.environ.get('HOST', '0.0.0.0')
    is_dev = os.environ.get('ENV', None) == 'dev'
    if host == '0.0.0.0':
        host = '127.0.0.1'
    app.run(host=host, port=port_number, debug=is_dev)