from flask import Flask, request
import threading
import requests

from authentication_broker.app import *


app = Flask(__name__)
auth_broker_url = 'http://127.0.0.1:5000/'
auth_broker_thread = threading.Thread(target=auth_app.run, args=[], kwargs={'host': '0.0.0.0', 'port': 5000})


@app.route('/auth/<path:varargs>', methods=['GET', 'POST'])
@app.route('/auth', methods=['GET', 'POST'])
def auth_broker_proxy(varargs=''):
    if request.method == 'GET':
        return requests.get(auth_broker_url + varargs, headers=request.headers, params=request.args).text
    else:
        return requests.post(auth_broker_url + varargs, headers=request.headers, data=request.form).text


if __name__ == '__main__':
    auth_broker_thread.start()
    app.run(host='0.0.0.0', port=9999, debug=True)
