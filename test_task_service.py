from suds.client import Client



print("~~place order~~")
logistic_client = Client('http://localhost:5005/?wsdl')
order_request_array = logistic_client.factory.create("s0:OrderRequestArray")
order_request = logistic_client.factory.create("s0:OrderRequest")
order_request.sender_secret_key = 'OWJytwsEELQIsrnSbTonZrETDQDLkV'
order_request.from_lat = -6.99999
order_request.from_lng = 128.000323
order_request.destination = "-6.0000,128.0000"
order_request.weight = 5.40
order_request.receiver_name = "Fahmi"
order_request.additional_detail = "Fahmi ampas"
order_request_array.OrderRequest.append(order_request)
print(logistic_client.service.place_order(order_request_array))

print("\n\n~~wallet~~")
logistic_client = Client('http://localhost:5006/?wsdl')
balance_request = logistic_client.factory.create("s0:BalanceRequest")
balance_request.secret_key = 'OWJytwsEELQIsrnSbTonZrETDQDLkV'
print(logistic_client.service.get_balance(balance_request))

withdraw_request = logistic_client.factory.create("s0:WithdrawRequest")
withdraw_request.secret_key = 'OWJytwsEELQIsrnSbTonZrETDQDLkV'
withdraw_request.bank_detail = '23523423423'
withdraw_request.payment_method = 'Transfer BCA'
withdraw_request.amount = 50000
print(logistic_client.service.withdraw(withdraw_request))

deposit_request = logistic_client.factory.create("s0:DepositRequest")
deposit_request.secret_key = 'OWJytwsEELQIsrnSbTonZrETDQDLkV'
deposit_request.bank_detail = '23523423423'
deposit_request.payment_method = 'Transfer BCA'
deposit_request.amount = 50000
print(logistic_client.service.deposit(deposit_request))


print("\n\n~~tracking~~")
logistic_client = Client('http://localhost:5007/?wsdl')
print("debug1")
tracking_request = logistic_client.factory.create("s0:TrackingRequest")
print("debug1")
tracking_request.order_unique_id = 'SvVoUHuZfuSOuTuNVXgeSjVTvieEHp'
tracking_request.secret_key = 'OWJytwsEELQIsrnSbTonZrETDQDLkV'
print(logistic_client.service.get_tracking(tracking_request))





