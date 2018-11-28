from suds.client import Client
from time import sleep
print("\n\n~~current_balance~~")
# logistic_client = Client('http://localhost:5006/?wsdl')
logistic_client = Client('http://111.221.44.148:1402/service/wallet?wsdl')
balance_request = logistic_client.factory.create("s0:BalanceRequest")
balance_request.secret_key = 'vIywNgjTJTNwIHZCXyHTZgfBepWwCx'
print(logistic_client.service.get_balance(balance_request))

print("\n\n~~withdraw~~")
withdraw_request = logistic_client.factory.create("s0:WithdrawRequest")
withdraw_request.secret_key = 'vIywNgjTJTNwIHZCXyHTZgfBepWwCx'
withdraw_request.bank_detail = '23523423423'
withdraw_request.payment_method = 'Transfer BCA'
withdraw_request.amount = 10000
print(logistic_client.service.withdraw(withdraw_request))
print(logistic_client.service.confirm_withdraw(withdraw_request))

sleep(5)

print("\n\n~~deposit~~")
deposit_request = logistic_client.factory.create("s0:DepositRequest")
deposit_request.secret_key = 'vIywNgjTJTNwIHZCXyHTZgfBepWwCx'
deposit_request.bank_detail = '23523423423'
deposit_request.payment_method = 'Transfer BCA'
deposit_request.amount = 50000
print(logistic_client.service.deposit(deposit_request))
print(logistic_client.service.confirm_deposit(deposit_request))

sleep(30)

print("\n\n~~current_balance~~")
logistic_client = Client('http://111.221.44.148:1402/service/wallet?wsdl')
# logistic_client = Client('http://localhost:5006/?wsdl')
balance_request = logistic_client.factory.create("s0:BalanceRequest")
balance_request.secret_key = 'vIywNgjTJTNwIHZCXyHTZgfBepWwCx'
print(logistic_client.service.get_balance(balance_request))
