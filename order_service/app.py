from flask import Flask, jsonify, request
import requests

from order_service.model import *

from pprint import pprint


auth_broker_url = 'http://127.0.0.1:9999/auth'
order_app = Flask(__name__)


@order_app.before_request
def _db_connect():
    if db.is_closed():
        db.connect()


@order_app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()

@order_app.route('/', methods=['GET'])
def get_order():
    response = requests.get(auth_broker_url, headers=request.headers).json()
    if response.get('error'):
        return jsonify({
            'error': 'Auth failed'
        })

    order = Order.get_or_none(order.id == response.get('id'))

    if order is None:
        return jsonify({
            'error': 'Order with that ID is not found'
        })

    return jsonify(customer.serialize())


@order_app.route('/', methods=['POST'])
def create_order():
    order = Order(
        id=request.form.get('id'),
        cust_id=request.form.get('cust_id'),
        emp_id=request.form.get('emp_id')
    )

    pprint(vars(order))

    try:
        order.save()
    except:
        return jsonify({
            'error': 'Missing one or more field'
        })

    data = {**order.serialize()}

    return jsonify(data)