from spyne import *
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import requests
from time import sleep

BASE_URL = 'http://127.0.0.1:9999/'

ComplexModel.Attributes.declare_order = "declared"


class OrderRequest(ComplexModel):
    sender_secret_key = String
    from_lat = Double
    from_lng = Double
    destination = String
    weight = Double
    receiver_name = String
    additional_detail = String


class OrderResponse(ComplexModel):
    status = String
    order_unique_id = String


class OrderService(ServiceBase):
    @rpc(Iterable(OrderRequest), _returns=Iterable(OrderResponse))
    def place_order(ctx, order_requests):
        '''order_requests = list(order_requests)
        grouped_requests = {}
        for order_request in order_requests:
            if grouped_requests.get(order_request.sender_secret_key) is None:
                grouped_requests[order_request.sender_secret_key] = []

            grouped_requests[order_request.sender_secret_key].append(order_request)

        responses = []

        for key, order_requests in grouped_requests.items():
            headers = {'Authorization': order_requests[0].sender_secret_key}
            data = {
                'emp_id': 1,
                "from_lat": order_requests[0].from_lat,
                'from_lng': order_requests[0].from_lng,
                'additional_detail': '',
                'items': []
            }
            for order_request in order_requests:
                item = {
                    "receiver_name": order_request.receiver_name,
                    'weight': order_request.weight,
                    'to_lat': float(order_request.destination.split(',')[0]),
                    'to_lng': float(order_request.destination.split(',')[1])
                }

                data['additional_detail'] += order_request.additional_detail

                data['items'].append(item)

            response = requests.post(BASE_URL + 'order', json=data, headers={'Authorization' : order_requests[0].sender_secret_key}).json()
            for _ in range(len(order_requests)):
                if response.get('error'):
                    responses.append(OrderResponse(
                        status="Fail: "+response.get('error'),
                        order_unique_id="fail" #response['unique_id']
                    ))
                else:
                    responses.append(OrderResponse(
                        status="Success",
                        order_unique_id=response['unique_id']
                    ))

        return responses'''
        order_requests = list(order_requests)

        data = {
            "variables": {
                "secret_key":{
                    "value": order_requests[0].sender_secret_key,
                    "type":"string"
                },
                "from_lat": {
                    "value": order_requests[0].from_lat,
                    "type":"double"
                },
                "from_lng": {
                    "value": order_requests[0].from_lng,
                    "type":"double"
                },
                "destination": {
                    "value": order_requests[0].destination,
                    "type":"string"
                },
                "weight": {
                    "value": order_requests[0].weight,
                    "type":"double"
                },
                "receiver_name": {
                    "value": order_requests[0].receiver_name,
                    "type":"string"
                },
                "additional_detail": {
                    "value": order_requests[0].additional_detail,
                    "type":"string"
                }
            }
        }

        r = requests.post('http://localhost:8080/engine-rest/process-definition/key/Process_1/tenant-id/1/start', json=data)
        r = r.json()
        sleep(2)
        r  = requests.get('http://localhost:9999/order', headers={'Authorization' : order_requests[0].sender_secret_key})
        r = r.json()
        return [OrderResponse(
            status="Success",
            order_unique_id=r[-1]['unique_id']
        )]


place_order_app = Application([OrderService],
                              tns='soa.logistic.order',
                              in_protocol=Soap11(validator='lxml'),
                              out_protocol=Soap11()
)

wsgi_place_order = WsgiApplication(place_order_app)
place_order_server = make_server('0.0.0.0', 5005, wsgi_place_order)