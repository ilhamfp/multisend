from suds.client import Client
print("~~place order~~")
logistic_client = Client('http://111.221.44.148:1402/service/place-order?wsdl')
order_request_array = logistic_client.factory.create("s0:OrderRequestArray")
order_request = logistic_client.factory.create("s0:OrderRequest")
order_request.sender_secret_key = 'vIywNgjTJTNwIHZCXyHTZgfBepWwCx'
order_request.from_lat = -6.000000
order_request.from_lng = 128.000323
order_request.destination = "-6.0000,89.0000"
order_request.weight = 5.40
order_request.receiver_name = "Ilham"
order_request.additional_detail = "Sepatu"
order_request_array.OrderRequest.append(order_request)
print(logistic_client.service.place_order(order_request_array))

