from flask import Flask, jsonify, request
import requests

from balance_service.model import *


auth_broker_url = 'http://127.0.0.1:9999/auth'
balance_app = Flask(__name__)


@balance_app.before_request
def _db_connect():
    if db.is_closed():
        db.connect()


@balance_app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


@balance_app.route('/', methods=['GET'])
def get_balance():
    response = requests.get(auth_broker_url, headers= request.headers).json()
    if response.get('error'):
        return jsonify({
            'error': 'User not found'
        })

    balance = Balance.get_or_none(Balance.user_id == response.get('id'))

    if balance is None:
        return jsonify({
            'error': 'Balance for that user is not found'
        })

    return jsonify(balance.serialize())


@balance_app.route('/', methods=['POST'])
def create_balance():
    response = requests.get(auth_broker_url, headers=request.headers)
    response = response.json()
    if response.get('error'):
        return jsonify({
            'error': 'User not found'
        })

    balance = Balance.get_or_none(Balance.user_id == response.get('id'))
    if balance:
        return jsonify({
            'error': 'Balance instance already exists'
        })

    balance = Balance(user_id=response.get('id'))
    balance.save()

    return jsonify(balance.serialize())


@balance_app.route('/withdraw', methods=['POST'])
def withdraw_balance():
    response = requests.get(auth_broker_url, headers=request.headers).json()
    if response.get('error'):
        return jsonify({
            'error': 'User not found'
        })

    balance = Balance.get_or_none(Balance.user_id == response.get('id'))

    if balance is None:
        return jsonify({
            'error': 'Balance for that user is not found'
        })

    amount = request.json.get('amount')

    if amount > balance.balance:
        return jsonify({
            'error': 'Balance not enough'
        })
    balance.balance -= amount
    balance.save()

    return jsonify(balance.serialize())

@balance_app.route('/deposit', methods=['POST'])
def deposit_balance():
    response = requests.get(auth_broker_url, headers=request.headers).json()
    if response.get('error'):
        return jsonify({
            'error': 'User not found'
        })

    balance = Balance.get_or_none(Balance.user_id == response.get('id'))

    if balance is None:
        return jsonify({
            'error': 'Balance for that user is not found'
        })

    amount = request.json.get('amount')

    if amount < 0:
        return jsonify({
            'error': 'Amount must be a non-negative integer'
        })

    balance.balance += amount
    balance.save()

    return jsonify(balance.serialize())

