from suds.client import Client

print("~~place order~~")
logistic_client = Client('http://localhost:5005/?wsdl')
order_request_array = logistic_client.factory.create("s0:OrderRequestArray")
order_request = logistic_client.factory.create("s0:OrderRequest")
order_request.sender_secret_key = 'vIywNgjTJTNwIHZCXyHTZgfBepWwCx'
order_request.from_lat = -6.99999
order_request.from_lng = 128.000323
order_request.destination = "-6.0000,128.0000"
order_request.weight = 5.40
order_request.receiver_name = "Tayo"
order_request.additional_detail = "Kolor tayo"
order_request_array.OrderRequest.append(order_request)
print(logistic_client.service.place_order(order_request_array))