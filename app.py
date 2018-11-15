from flask import Flask, request
import threading
import requests

from authentication_broker.app import *
from balance_service.app import *


app = Flask(__name__)
auth_broker_url = 'http://127.0.0.1:5000/'
auth_broker_thread = threading.Thread(target=auth_app.run, args=[], kwargs={'host': '127.0.0.1', 'port': 5000})

balance_service_url = 'http://127.0.0.1:5001/'
balance_service_thread = threading.Thread(target=balance_app.run, args=[], kwargs={'host': '127.0.0.1', 'port': 5001})


@app.route('/auth', methods=['GET', 'POST'])
@app.route('/auth/<path:varargs>', methods=['GET', 'POST'])
def auth_broker_proxy(varargs=''):
    if request.method == 'GET':
        return requests.get(auth_broker_url + varargs, headers=request.headers, params=request.args).text
    else:
        return requests.post(auth_broker_url + varargs, headers=request.headers, data=request.form).text


@app.route('/balance', methods=['GET', 'POST'])
@app.route('/balance/<path:varargs>', methods=['GET', 'POST'])
def balance_proxy(varargs=''):
    if request.method == 'GET':
        return requests.get(balance_service_url + varargs, headers=request.headers, params=request.args).text
    else:
        return requests.post(balance_service_url + varargs, headers=request.headers, data=request.form).text


if __name__ == '__main__':
    auth_broker_thread.start()
    balance_service_thread.start()
    app.run(host='127.0.0.1', port=9999)
