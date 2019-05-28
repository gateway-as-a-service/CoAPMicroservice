import json

from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP
from walrus import Walrus

from config import REDIS_HOSTNAME, REDIS_PORT


class DevicesResource(Resource):
    DEVICES_MESSAGES_QUEUE = "devices_messages"

    def __init__(self, logger, name="DevicesResource"):
        super(DevicesResource, self).__init__(name)

        self.logger = logger

        self.walrus = Walrus(REDIS_HOSTNAME, REDIS_PORT)
        self.messages_from_devices_queue = self.walrus.List(self.DEVICES_MESSAGES_QUEUE)

    def render_PUT(self, request):
        message = json.loads(request.payload)
        self.logger.info("Received message: {}".format(message))

        self._forward_message_from_device(message)
        self.logger.info("Message has been send to the processing step")

        return self

    def render_GET(self, request):
        pass

    def render_GET_advanced(self, request, response):
        pass

    def render_PUT_advanced(self, request, response):
        pass

    def render_POST(self, request):
        pass

    def render_POST_advanced(self, request, response):
        pass

    def render_DELETE(self, request):
        pass

    def render_DELETE_advanced(self, request, response):
        pass

    def _forward_message_from_device(self, message):
        """
        Used to forward the received message by the micro-service the MessageProcessor Component
        :param message:
        :return:
        """
        self.messages_from_devices_queue.append(json.dumps(message))


class CoAPServer(CoAP):
    def __init__(self, host, port, logger):
        super().__init__((host, port))
        self.add_resource('devices/', DevicesResource(logger))
