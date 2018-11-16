from flask import Flask, jsonify, request
import requests

from employee_service.model import *

auth_broker_url = 'http://127.0.0.1:9999/auth'
employee_app = Flask(__name__)

@employee_app.before_request
def _db_connect():
    if db.is_closed():
        db.connect()


@employee_app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


@employee_app.route('/', methods=['GET'])
def get_employee():
    response = requests.get(auth_broker_url, headers= request.headers).json()
    if response.get('error'):
        return jsonify({
            'error': 'User not found'
        })

    employee = Employee.get_or_none(Employee.user_id == response.get('id'))

    if employee is None:
        return jsonify({
            'error': 'Employee for that user is not found'
        })

    return jsonify(employee.serialize())


@employee_app.route('/', methods=['POST'])
def register():
    response = requests.post(auth_broker_url, headers=request.headers, data=request.form).json()
    if response.get('error'):
        return jsonify({
            'error': 'Fail creating employee account'
        })

    employee = Employee(
        user_id=response.get('id'),
        first_name=request.form.get('first_name'),
        last_name=request.form.get('last_name'),
        bank_name=request.form.get('bank_name')
        bank_account_number = request.form.get('bank_account_number'),
        phone_number = request.form.get('phone_number'),
    )

    try:
        employee.save()
    except:
        return jsonify({
            'error': 'Missing one or more field'
        })

    data = {**employee.serialize()}
    data['access_token'] = response.get('access_token')

    return jsonify(data)