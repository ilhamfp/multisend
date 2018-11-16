from flask import Flask, jsonify, request
import requests

from authentication_broker.model import *

balance_service_url = 'http://127.0.0.1:9999/balance'
auth_app = Flask(__name__)


@auth_app.before_request
def _db_connect():
    if db.is_closed():
        db.connect()


@auth_app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


@auth_app.route('/', methods=['GET'])
def get_user():
    access_token = request.headers.get('Authorization')
    user = User.get_or_none(User.access_token == access_token)

    if user is None:
        return jsonify({
            'error': 'User not found'
        })

    return jsonify(user.serialize())


@auth_app.route('/', methods=['POST'])
def register_user():
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.get_or_none(User.email == email)
    if user is not None:
        return jsonify({
            'error': 'User already exists'
        })

    user = User(email=email, password=password)
    user.save()

    response = requests.post(balance_service_url, headers={'Authorization': user.access_token})
    response = response.json()

    if response.get('error'):
        user.delete_instance()
        return jsonify({
            'error': 'Fail creating user'
        })

    return jsonify(user.serialize())
