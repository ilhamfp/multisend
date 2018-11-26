from spyne import *
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import requests

BASE_URL = 'http://127.0.0.1:9999/'

ComplexModel.Attributes.declare_order = "declared"


class BalanceRequest(ComplexModel):
    secret_key = String


class WithdrawRequest(ComplexModel):
    secret_key = String
    bank_detail = String
    payment_method = String
    amount = Integer


class DepositRequest(ComplexModel):
    secret_key = String
    bank_detail = String
    payment_method = String
    amount = Integer


class NotificationResponse(ComplexModel):
    status = String
    current_balance = Integer


class PaymentGatewayResponse(ComplexModel):
    status = String


class WalletService(ServiceBase):
    @rpc(BalanceRequest, _returns=NotificationResponse)
    def get_balance(ctx, request):
        r = requests.get(BASE_URL + "balance", headers={'Authorization' : request.secret_key})
        result = r.json()
        return NotificationResponse(
            status="Success",
            current_balance=result['balance']
        )

    @rpc(WithdrawRequest, _returns=NotificationResponse)
    def withdraw(ctx, request):
        data = {
            "variables": {
                "secret_key":{
                    "value": request.secret_key,
                    "type":"string"
                },
                "amount": {
                    "value":request.amount,
                    "type":"long"
                },
                "bank": {
                    "value":request.bank_detail,
                    "type":"string"
                },
                "payment_method": {
                    "value":request.payment_method,
                    "type":"string"
                }
            }
        }

        r = requests.get(BASE_URL + "balance", headers={'Authorization': request.secret_key})
        result = r.json()

        r = requests.post('http://localhost:8080/engine-rest/process-definition/key/Process_1/tenant-id/2/start', json=data)
        return NotificationResponse(
            status="Success",
            current_balance=result['balance'] - request.amount
        )

    @rpc(WithdrawRequest, _returns=PaymentGatewayResponse)
    def confirm_withdraw(ctx, request):
        data = {
            "messageName" : "receive_confirmation",
            "tenantId" : "2",
            "correlationKeys" : {
                    "bank" : {"value" : request.bank_detail, "type": "String"}
                  },
            "processVariables" : {
                "success" : {"value" : "true", "type": "boolean"}
            }
        }

        r = requests.post('http://localhost:8080/engine-rest/message', json=data)

        return PaymentGatewayResponse(status="Success")

    @rpc(DepositRequest, _returns=NotificationResponse)
    def deposit(ctx, request):
        data = {
            "variables": {
                "secret_key":{
                    "value": request.secret_key,
                    "type":"string"
                },
                "amount": {
                    "value":request.amount,
                    "type":"long"
                },
                "bank": {
                    "value":request.bank_detail,
                    "type":"string"
                },
                "payment_method": {
                    "value":request.payment_method,
                    "type":"string"
                }
            }
        }

        r = requests.get(BASE_URL + "balance", headers={'Authorization': request.secret_key})
        result = r.json()

        r = requests.post('http://localhost:8080/engine-rest/process-definition/key/deposit-process/tenant-id/3/start',
                          json=data)
        return NotificationResponse(
            status="Success",
            current_balance=result['balance'] + request.amount
        )

    @rpc(DepositRequest, _returns=PaymentGatewayResponse)
    def confirm_deposit(ctx, request):
        data = {
            "messageName" : "receive_deposit_confirm",
            "tenantId" : "3",
            "correlationKeys" : {
                    "bank" : {"value" : request.bank_detail, "type": "String"}
                  },
            "processVariables" : {
                "success" : {"value" : "true", "type": "boolean"}
            }
        }

        r = requests.post('http://localhost:8080/engine-rest/message', json=data)

        return PaymentGatewayResponse(status="Success")


wallet_app = Application([WalletService],
                         tns='soa.logistic.wallet',
                         in_protocol=Soap11(validator='lxml'),
                         out_protocol=Soap11()
)

wsgi_wallet = WsgiApplication(wallet_app)
wallet_server = make_server('0.0.0.0', 5006, wsgi_wallet)