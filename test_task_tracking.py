from suds.client import Client
print("\n\n~~tracking~~")
logistic_client = Client('http://111.221.44.148:1402/service/tracking?wsdl')
tracking_request_array = logistic_client.factory.create("s0:TrackingRequestArray")
tracking_request = logistic_client.factory.create("s0:TrackingRequest")
tracking_request.order_unique_id = 'SvVoUHuZfuSOuTuNVXgeSjVTvieEHp'
tracking_request.secret_key = 'vIywNgjTJTNwIHZCXyHTZgfBepWwCx'
tracking_request_array.TrackingRequest.append(tracking_request)
print(logistic_client.service.get_tracking(tracking_request_array))