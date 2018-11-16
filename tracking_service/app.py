from spyne import *
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import requests

BASE_URL = 'http://127.0.0.1:9999/'

class TrackingRequest(ComplexModel):
    order_unique_id = String


class TrackingResponse(ComplexModel):
    status = String
    current_location = String
    additional_detail = String


class TrackingService(ServiceBase):
    @rpc(Iterable(TrackingRequest), _returns=Iterable(TrackingResponse))
    def get_tracking(ctx, tracking_request):
        response = requests.get(BASE_URL + "/order/" + tracking_request.order_unique_id, headers={'Authorization' : request.secret_key}).json()
        all_points = [x for x in response['points']]
        points = list(filter(lambda x: x['status'], [x for x in response['points']]))
        if response.get('error'):
            return TrackingResponse(
                status = "error",
                current_location = "error",
                additional_detail = "error"
            )
        else:
            return TrackingResponse(
                status = str(len(points))+"/"+str(len(all_points))+" have been delivered",
                current_location = "{"+str(response['points'][0]['lat'])+"}, {"+str(response['points'][0]['lng'])+"}",
                additional_detail = response['points'][0]['status']
            )


tracking_app = Application([TrackingService],
                              tns='soa.logistic.tracking',
                              in_protocol=Soap11(validator='lxml'),
                              out_protocol=Soap11()
)

wsgi_tracking = WsgiApplication(tracking_app)
tracking_server = make_server('0.0.0.0', 5007, wsgi_tracking)