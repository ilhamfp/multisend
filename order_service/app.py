from flask import Flask, jsonify, request
import requests

from order_service.model import *


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
            'error': 'Invalid Auth'
        })

    orders = Order.select().where(Order.cust_id == response.get('id'))

    data = [order.serialize() for order in orders]

    return jsonify(data)


@order_app.route('/<unique_id>', methods=['GET'])
def get_order_by_unique_id(unique_id):
    order = Order.get_or_none(Order.unique_id == unique_id)

    if order is None:
        return jsonify({
            'error' : 'Order not found'
        })

    return jsonify(order.serialize())


@order_app.route('/', methods=['POST'])
def create_order():
    if len(request.json.get('items')) == 0:
        return jsonify({
            'error': 'You must specify at least 1 item'
        })

    response = requests.get(auth_broker_url, headers=request.headers).json()
    if response.get('error'):
        return jsonify({
            'error': 'Invalid Auth'
        })

    order = Order(
        cust_id=response.get('id'),
        emp_id=request.json.get('emp_id'),
        from_lat=request.json.get('from_lat'),
        from_lng=request.json.get('from_lng'),
        additional_detail=request.json.get('additional_detail')
    )

    try:
        order.save()
    except Exception as e:
        print(e)
        return jsonify({
            'error': 'Missing one or more field'
        })

    for item in request.json.get('items'):
        order_point = OrderPoint(
            order=order,
            receiver_name=item['receiver_name'],
            to_lat=item['to_lat'],
            to_lng=item['to_lng'],
            weight=item['weight']
        )

        order_point.save()

    data = {**order.serialize()}

    return jsonify(data)