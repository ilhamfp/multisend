from flask import Flask, request
import threading
import requests

from authentication_broker.app import *
from balance_service.app import *
from customer_service.app import *
from employee_service.app import *
from order_service.app import *
from place_order_service.app import *
from tracking_service.app import *
from wallet_service.app import *

app = Flask(__name__)
auth_broker_url = 'http://127.0.0.1:5000/'
auth_broker_thread = threading.Thread(target=auth_app.run, args=[], kwargs={'host': '127.0.0.1', 'port': 5000, 'threaded': True})

balance_service_url = 'http://127.0.0.1:5001/'
balance_service_thread = threading.Thread(target=balance_app.run, args=[], kwargs={'host': '127.0.0.1', 'port': 5001, 'threaded': True})

customer_service_url = 'http://127.0.0.1:5002/'
customer_service_thread = threading.Thread(target=customer_app.run, args=[], kwargs={'host': '127.0.0.1', 'port': 5002, 'threaded': True})

employee_service_url = 'http://127.0.0.1:5003/'
employee_service_thread = threading.Thread(target=employee_app.run, args=[], kwargs={'host': '127.0.0.1', 'port': 5003, 'threaded': True})

order_service_url = 'http://127.0.0.1:5004/'
order_service_thread = threading.Thread(target=order_app.run, args=[], kwargs={'host': '127.0.0.1', 'port': 5004,  'threaded': True})

wallet_service_url = 'http://127.0.0.1:5006/'
wallet_service_thread = threading.Thread(target=wallet_server.serve_forever, args=[], kwargs={})

place_order_service_url = 'http://127.0.0.1:5005/'
place_order_service_thread = threading.Thread(target=place_order_server.serve_forever, args=[], kwargs={})

tracking_service_url = 'http://127.0.0.1:5007/'
tracking_service_thread = threading.Thread(target=tracking_server.serve_forever, args=[], kwargs={})


@app.route('/auth', methods=['GET', 'POST'])
@app.route('/auth/<path:varargs>', methods=['GET', 'POST'])
def auth_broker_proxy(varargs=''):
    if request.method == 'GET':
        response = requests.get(auth_broker_url + varargs, headers=request.headers, params=request.args)
    else:
        response = requests.post(auth_broker_url + varargs, headers=request.headers, json=request.json)

    return response.text, dict(response.headers)


@app.route('/balance', methods=['GET', 'POST'])
@app.route('/balance/<path:varargs>', methods=['GET', 'POST'])
def balance_proxy(varargs=''):
    if request.method == 'GET':
        response = requests.get(balance_service_url + varargs, headers=request.headers, params=request.args)
    else:
        print(varargs)
        response = requests.post(balance_service_url + varargs, headers=request.headers, json=request.json)

    return response.text, dict(response.headers)


@app.route('/customer', methods=['GET', 'POST'])
@app.route('/customer/<path:varargs>', methods=['GET', 'POST'])
def customer_proxy(varargs=''):
    if request.method == 'GET':
        response = requests.get(customer_service_url + varargs, headers=request.headers, params=request.args)
    else:
        response = requests.post(customer_service_url + varargs, headers=request.headers, json=request.json)

    return response.text, dict(response.headers)


@app.route('/employee', methods=['GET', 'POST'])
@app.route('/employee/<path:varargs>', methods=['GET', 'POST'])
def employee_proxy(varargs=''):
    if request.method == 'GET':
        response = requests.get(employee_service_url + varargs, headers=request.headers, params=request.args)
    else:
        response = requests.post(employee_service_url + varargs, headers=request.headers, json=request.json)

    return response.text, dict(response.headers)


@app.route('/order', methods=['GET', 'POST'])
@app.route('/order/<path:varargs>', methods=['GET', 'POST'])
def order_proxy(varargs=''):
    if request.method == 'GET':
        response = requests.get(order_service_url + varargs, params=request.args, headers=request.headers)
    else:
        response = requests.post(order_service_url + varargs, headers=request.headers, json=request.json)

    return response.text, dict(response.headers)


@app.route('/place-order', methods=['GET', 'POST'])
def place_order_proxy():
    if request.method == 'GET':
        response = requests.get(place_order_service_url + '?wsdl', headers=request.headers)
    else:
        response = requests.post(place_order_service_url, headers=request.headers, data=request.data)

    return response.text, dict(response.headers)


@app.route('/wallet', methods=['GET', 'POST'])
def wallet_proxy():
    if request.method == 'GET':
        response = requests.get(wallet_service_url + '?wsdl', headers=request.headers)
    else:
        response = requests.post(wallet_service_url, headers=request.headers, data=request.data)

    return response.text, dict(response.headers)


@app.route('/tracking', methods=['GET', 'POST'])
def tracking_proxy():
    if request.method == 'GET':
        response = requests.get(tracking_service_url + '?wsdl', headers=request.headers)
    else:
        response = requests.post(tracking_service_url, headers=request.headers, data=request.data)

    return response.text, dict(response.headers)

if __name__ == '__main__':
    auth_broker_thread.start()
    balance_service_thread.start()
    customer_service_thread.start()
    employee_service_thread.start()
    order_service_thread.start()
    place_order_service_thread.start()
    wallet_service_thread.start()
    tracking_service_thread.start()
    app.run(host='127.0.0.1', port=9999, threaded=True)
