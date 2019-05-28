from coap_message_forward import COapMessageForward
import coap_server
from config import COAP_HOSTNAME, COAP_PORT
from utils import retrieve_logger


class MicroserviceBootstrap(object):

    def __init__(self):

        self.logger = retrieve_logger("coap_microservice")

        self.coap_message_forward = COapMessageForward(self.logger)
        self.logger.info("Host: {}; Port: {}".format(COAP_HOSTNAME, COAP_PORT))
        self.coap_server = coap_server.CoAPServer(COAP_HOSTNAME, COAP_PORT, self.logger)

    def start(self):
        self.coap_message_forward.start()

        try:
            self.coap_server.listen(10)
        except KeyboardInterrupt:
            self.logger.info("Server Shutdown")
            self.coap_server.close()
            self.logger.info("Closing....")


if __name__ == '__main__':
    microservice_bootstrap = MicroserviceBootstrap()
    microservice_bootstrap.start()
