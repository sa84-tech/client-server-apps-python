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
    def __init__(self, srv_address=DEFAULT_IP_ADDRESS, srv_port=DEFAULT_PORT, mode='listen', account_name='Guest'):
        super().__init__()
        self.srv_address = srv_address
        self.srv_port = srv_port
        self.account_name = account_name
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger = logging.getLogger('client')
        self.client_mode = mode

    def __str__(self):
        return f'Client is connected to {self.srv_address}:{self.srv_port}'

    @Log()
    def parse_message(self, message):
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
        text = input('Enter message (type @quit to exit): ')
        message = {
            ACTION: MESSAGE,
            TIME: time.time(),
            ACCOUNT_NAME: self.account_name,
            MESSAGE_TEXT: text
        }
        return message

    @Log()
    def start_send_mode(self):
        while True:
            message_to_send = self.create_message()
            if message_to_send[MESSAGE_TEXT] == '@quit':
                self.socket.close()
                self.logger.info('Shutdown by user command')
                print('Bye')
                sys.exit(0)
            try:
                self.send_message(self.socket, message_to_send)
            except ConnectionError:
                self.logger.error(f'Connection with server {self.srv_address} lost.')
                sys.exit(1)

    @Log()
    def start_listen_mode(self):
        while True:
            try:
                in_message = self.parse_message(self.get_message(self.socket))
                print(in_message)
            except ConnectionError:
                self.logger.error(f'Connection with server {self.srv_address} lost.')
                sys.exit(1)
            except (ValueError, json.JSONDecodeError):
                self.logger.error('Failed to decode server message')
                sys.exit(1)

    @Log()
    def connect(self):
        try:
            self.socket.connect((self.srv_address, self.srv_port))
            self.logger.info(self)
            init_message = self.create_init_message()
            self.send_message(self.socket, init_message)
            message = self.get_message(self.socket)
            response = self.parse_message(message)
            print(f'Connection established, Server: {self.socket.getpeername()}, Client: {self.socket.getsockname()}')
            print('Response from Server', response)
        except ConnectionError:
            self.logger.error('Connection failed')
        except (ValueError, json.JSONDecodeError):
            self.logger.error('Failed to decode server message')
        else:
            if self.client_mode == 'send':
                print('Client runs in SEND mode')
                self.start_send_mode()
            elif self.client_mode == 'listen':
                print('Client runs in LISTEN mode')
                self.start_listen_mode()
            else:
                print('Invalid mode status. Exiting...')
                sys.exit(1)


if __name__ == '__main__':
    def check_error(value, message):
        if value == -1:
            logger.critical(message)
            sys.exit(1)
        return value


    logger = logging.getLogger('client')

    address = check_error(*Messaging.get_address(sys.argv))
    port = check_error(*Messaging.get_port(sys.argv))
    mode = check_error(*Messaging.get_mode(sys.argv))
    name = check_error(*Messaging.get_name(sys.argv))

    client = Client(srv_address=address, srv_port=port, mode=mode, account_name=name)
    client.connect()
