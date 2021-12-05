import socket
import sys
import json
import logging

import log.server_log_config
from utils.constants import DEFAULT_PORT, MAX_CONNECTIONS, RESPONSE, ERROR, ACTION, USER, ACCOUNT_NAME, PRESENCE, TIME, \
    RESPONSE_DEFAULT_IP_ADDRESS
from utils.messaging import Messaging


class Server(Messaging):
    def __init__(self, ip_address='', port=DEFAULT_PORT):
        super().__init__()
        self.ip_address = ip_address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger = logging.getLogger('server')

    def __str__(self):
        return f'Server is running on port {self.port}'

    def parse_message(self, message):
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
                and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
            return {RESPONSE: 200}
        return {
            RESPONSE_DEFAULT_IP_ADDRESS: 400,
            ERROR: 'Bad Request'
        }

    def listen(self):
        self.socket.bind((self.ip_address, self.port))
        self.socket.listen(MAX_CONNECTIONS)
        self.logger.info(self)

        while True:
            client, client_addr = self.socket.accept()
            try:
                message = self.get_message(client)
                response = self.parse_message(message)
                self.send_message(client, response)
                self.logger.info(f'Message proccesed: {client}')
            except (ValueError, json.JSONDecodeError):
                self.logger.error(f'Bad request from client: {client}')
            finally:
                client.close()


if __name__ == '__main__':
    logger = logging.getLogger('Server')
    address, message = Messaging.get_address(sys.argv)
    if address == -1:
        logger.critical(message)
        sys.exit(1)

    port, message = Messaging.get_port(sys.argv)
    if port == -1:
        logger.critical(message)
        sys.exit(1)

    server = Server(address, port)
    server.listen()
