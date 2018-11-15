from flask import Flask, jsonify, request
from authentication_broker.model import *


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

    return user.serialize()


@auth_app.route('/', methods=['POST'])
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User(email=email, password=password)
    user.save()

    return user.serialize()
