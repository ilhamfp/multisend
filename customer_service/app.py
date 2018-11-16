from flask import Flask, jsonify, request
import requests

from customer_service.model import *


auth_broker_url = 'http://127.0.0.1:5000/'
customer_app = Flask(__name__)


@customer_app.before_request
def _db_connect():
    if db.is_closed():
        db.connect()


@customer_app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


@customer_app.route('/', methods=['GET'])
def get_customer():
    response = requests.get(auth_broker_url, headers=request.headers).json()
    if response.get('error'):
        return jsonify({
            'error': 'User not found'
        })

    customer = Customer.get_or_none(Customer.user_id == response.get('id'))

    if customer is None:
        return jsonify({
            'error': 'Customer for that user is not found'
        })

    return jsonify(customer.serialize())


@customer_app.route('/', methods=['POST'])
def register():
    response = requests.post(auth_broker_url, headers=request.headers, json=request.json).json()
    if response.get('error'):
        return jsonify({
            'error': 'Fail creating customer account'
        })

    customer = Customer(
        user_id=response.get('id'),
        first_name=request.json.get('first_name'),
        last_name=request.json.get('last_name')
    )

    try:
        customer.save()
    except:
        return jsonify({
            'error': 'Missing one or more field'
        })

    data = {**customer.serialize()}
    data['access_token'] = response.get('access_token')

    return jsonify(data)