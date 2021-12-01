import sys
import socket
import json
import time

from utils.constants import DEFAULT_PORT, DEFAULT_IP_ADDRESS, RESPONSE, ERROR, ACTION, PRESENCE, TIME, USER, \
    ACCOUNT_NAME

from utils.messaging import Messaging


class Client(Messaging):
    def __init__(self, srv_address=DEFAULT_IP_ADDRESS, srv_port=DEFAULT_PORT, account_name='Guest'):
        super().__init__()
        self.srv_address = srv_address
        self.srv_port = srv_port
        self.account_name = account_name
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __str__(self):
        return f'Client is connected to {self.srv_address}:{self.srv_port}'

    def parse_message(self, message):
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return '200 : OK'
            return f'400 : {message[ERROR]}'
        raise ValueError

    def create_init_message(self):
        message = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.account_name
            }
        }
        return message

    def connect(self):
        try:
            self.socket.connect((self.srv_address, self.srv_port))
            print(self)
            init_message = self.create_init_message()
            self.send_message(self.socket, init_message)
            message = self.get_message(self.socket)
            response = self.parse_message(message)
            print(response)
        except ConnectionError:
            print('Connection failed')
        except (ValueError, json.JSONDecodeError):
            print('Failed to decode server message')


if __name__ == '__main__':
    address = Messaging.get_address(sys.argv)
    if address == -1:
        sys.exit(1)

    port = Messaging.get_port(sys.argv)
    if port == -1:
        sys.exit(1)

    client = Client(address, port)
    client.connect()
