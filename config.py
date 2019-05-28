import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

print(os.environ.get('APP_ENV'))
if os.environ.get('APP_ENV') == 'docker':
    REDIS_HOSTNAME = "docker.for.win.localhost"
else:
    REDIS_HOSTNAME = "127.0.0.1"

REDIS_PORT = 6379
COAP_PORT = 5683
COAP_HOSTNAME = "0.0.0.0"

DEVICES_MESSAGES_QUEUE = "devices_messages"
