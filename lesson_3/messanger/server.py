import socket
import sys
import json

from utils.constants import DEFAULT_PORT, MAX_CONNECTIONS, RESPONSE, ERROR, ACTION, USER, ACCOUNT_NAME, PRESENCE, TIME, \
    RESPONSE_DEFAULT_IP_ADDRESS
from utils.messaging import Messaging


class Server(Messaging):
    def __init__(self, ip_address='', port=DEFAULT_PORT):
        super().__init__()
        self.ip_address = ip_address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        print(self)

        while True:
            client, client_addr = self.socket.accept()
            try:
                message = self.get_message(client)
                print(message)
                response = self.parse_message(message)
                self.send_message(client, response)
            except (ValueError, json.JSONDecodeError):
                print(f'Bad request from client: {client}')
            finally:
                client.close()


if __name__ == '__main__':
    address = Messaging.get_address(sys.argv)
    if address == -1:
        sys.exit(1)

    port = Messaging.get_port(sys.argv)
    if port == -1:
        sys.exit(1)

    server = Server(address, port)
    server.listen()
