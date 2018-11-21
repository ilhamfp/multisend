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
        print(request)
        data = {
            "bank": request.bank_detail,
            "payment_method": request.payment_method,
            "amount": request.amount
        }

        r = requests.post(BASE_URL + "balance/withdraw", headers={'Authorization': request.secret_key}, json=data)
        result = r.json()
        if result.get('error') is None:
            r = requests.get(BASE_URL + "balance", headers={'Authorization': request.secret_key})
            result = r.json()
            return NotificationResponse(
                status="Success",
                current_balance=result['balance']
            )

    @rpc(DepositRequest, _returns=NotificationResponse)
    def deposit(ctx, request):
        print(request)
        data = {
            "bank": request.bank_detail,
            "payment_method": request.payment_method,
            "amount": request.amount
        }
        r = requests.post(BASE_URL + "balance/deposit", headers={'Authorization': request.secret_key}, json=data)
        result = r.json()
        if result.get('error') is None:
            r = requests.get(BASE_URL + "balance", headers={'Authorization': request.secret_key})
            result = r.json()
            return NotificationResponse(
                status="Success",
                current_balance=result['balance']
            )


wallet_app = Application([WalletService],
                         tns='soa.logistic.wallet',
                         in_protocol=Soap11(validator='lxml'),
                         out_protocol=Soap11()
)

wsgi_wallet = WsgiApplication(wallet_app)
wallet_server = make_server('0.0.0.0', 5006, wsgi_wallet)