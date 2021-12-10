import logging
import sys
import socket
import json
import time

from utils.decorators import Log
from utils.constants import DEFAULT_PORT, DEFAULT_IP_ADDRESS, RESPONSE, ERROR, ACTION, PRESENCE, TIME, USER, \
    ACCOUNT_NAME, MESSAGE, SENDER
from utils.messaging import Messaging

from messanger.utils.constants import MESSAGE, MESSAGE_TEXT


class Client(Messaging):
    def __init__(self, srv_address=DEFAULT_IP_ADDRESS, srv_port=DEFAULT_PORT, mode='send', account_name='Client1'):
        super().__init__()
        self.srv_address = srv_address
        self.srv_port = srv_port
        self.account_name = account_name
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.logger = logging.getLogger('client')
        self.client_mode = mode

    def __str__(self):
        return f'Client is connected to {self.srv_address}:{self.srv_port}'

    @Log()
    def parse_message(self, message):
        # print('parse_message', message)
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return '200 : OK'
            self.logger.warning(f'400 : {message[ERROR]}')
            return f'400 : {message[ERROR]}'
        elif ACTION in message and message[ACTION] == MESSAGE:
            return f'Incoming message from user {message[SENDER]}:\n{message[MESSAGE_TEXT]}'
        raise ValueError

    @Log()
    def create_init_message(self):
        message = {
            ACTION: PRESENCE,
            TIME: time.time(),
            ACCOUNT_NAME: self.account_name
        }
        return message

    @Log()
    def create_message(self):
        text = "Hi, how is it going?"
        message = {
            ACTION: MESSAGE,
            TIME: time.time(),
            ACCOUNT_NAME: self.account_name,
            MESSAGE_TEXT: text
        }
        return message

    @Log()
    def connect(self):
        try:
            self.socket.connect((self.srv_address, self.srv_port))
            self.logger.info(self)
            init_message = self.create_init_message()
            self.send_message(self.socket, init_message)
            message = self.get_message(self.socket)
            response = self.parse_message(message)
            print('RESPONSE', response)
        except ConnectionError:
            self.logger.error('Connection failed')
        except (ValueError, json.JSONDecodeError):
            self.logger.error('Failed to decode server message')
        else:
            if self.client_mode == 'send':
                print('Client runs in send mode', self.socket)
            elif self.client_mode == 'listen':
                print('Client runs in listen mode', self.socket)
            while True:
                if self.client_mode == 'send':
                    try:
                        send_message = self.create_message()
                        self.send_message(self.socket, send_message)
                        time.sleep(3)
                    except ConnectionError:
                        self.logger.error(f'Connection with server {self.srv_address} lost.')
                        sys.exit(1)

                elif self.client_mode == 'listen':

                    try:
                        self.parse_message(self.get_message(self.socket))
                        time.sleep(3)
                    except ConnectionError:
                        self.logger.error(f'Connection with server {self.srv_address} lost.')
                        sys.exit(1)
                    except (ValueError, json.JSONDecodeError):
                        self.logger.error('Failed to decode server message')
                        sys.exit(1)


if __name__ == '__main__':
    logger = logging.getLogger('client')
    address, message = Messaging.get_address(sys.argv)
    if address == -1:
        logger.critical(message)
        sys.exit(1)

    port, message = Messaging.get_port(sys.argv)
    if port == -1:
        logger.critical(message)
        sys.exit(1)

    client = Client(address, port)
    client.connect()
