import json
import threading
import time

from coapthon.client.helperclient import HelperClient
from walrus import Walrus

from config import REDIS_PORT, REDIS_HOSTNAME
from utils import retrieve_logger


class COapMessageForward(threading.Thread):
    CoAP_MESSAGE_INCOMING_QUEUE = "devices/coap"
    COAP_BASE_PORT = 5682

    MAX_ATTEMPTS = 10
    SLEEP_PERIOD = 3

    def __init__(self, logger):
        super().__init__(daemon=True)

        self.logger = logger

        self.walrus = Walrus(REDIS_HOSTNAME, REDIS_PORT)
        self.messages_to_be_send_to_devices_queue = self.walrus.List(self.CoAP_MESSAGE_INCOMING_QUEUE)

    @staticmethod
    def _get_coap_url(device_uuid):
        return "devices-{}".format(device_uuid)

    def _forward_to_device(self, device_info, device_value):
        device_uuid = device_info["device_uuid"]
        device_ip = device_info["ip"]
        device_coap_port = device_info.get("port") or self.COAP_BASE_PORT
        device_coap_url = self._get_coap_url(device_uuid)
        body = {
            "value": device_value,
        }

        attempts = 0
        while attempts < self.MAX_ATTEMPTS:
            self.logger.info("Attempt {}. Send message {} to coap server {}".format(attempts, device_value, device_ip))

            try:
                coap_client = HelperClient((device_ip, device_coap_port))
                response = coap_client.put(device_coap_url, json.dumps(body))
                if not response:
                    raise Exception("Failed to send the message to the device")

                self.logger.info("Message was sent to device")
                break

            except Exception as err:
                self.logger.error("Failed to send the message to the device {}. Reason: {}".format(device_uuid, err))
                self.logger.info("Sleep a period before retrying to send the message to device {}".format(device_uuid))

                attempts += 1
                time.sleep(self.SLEEP_PERIOD)

        if attempts == self.MAX_ATTEMPTS:
            raise Exception("Failed to forward the message")

    def run(self):
        self.logger.info("Waiting for messages to be sent to devices")
        while True:
            message = self.messages_to_be_send_to_devices_queue.bpopleft(timeout=120)
            if not message:
                continue

            message = json.loads(message.decode("utf-8"))
            self.logger.info("Received message from GASS that will be forwarded to the device. {}".format(message))

            try:
                self._forward_to_device(message["device_info"], message["value"])
            except Exception as err:
                self.logger.error(err, exc_info=True)
                continue

            self.logger.info("Wait for message...")


if __name__ == '__main__':
    coap_message_forward = COapMessageForward(retrieve_logger("coap_message_forward"))
    coap_message_forward.run()
