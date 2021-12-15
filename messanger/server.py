import socket
import sys
import logging
import time

import select
from utils.decorators import Log
from utils.constants import DEFAULT_PORT, MAX_CONNECTIONS, RESPONSE, ERROR, ACTION, USER, ACCOUNT_NAME, PRESENCE, TIME, \
    RESPONSE_DEFAULT_IP_ADDRESS, MESSAGE, SENDER, MESSAGE_TEXT
from utils.messaging import Messaging


class Server(Messaging):
    logger = logging.getLogger('server')
    clients = []
    clients_names = []  # [{name: User_name, message: Message_text},]
    messages = []

    def __init__(self, ip_address='', port=DEFAULT_PORT):
        super().__init__()
        self.ip_address = ip_address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __str__(self):
        return f'Server is running on port {self.port}'

    @Log()
    def parse_message(self, message):
        if ACTION in message:
            if message[ACTION] == PRESENCE and TIME in message and ACCOUNT_NAME in message:
                self.clients_names.append(message[ACCOUNT_NAME])
                print(message)
                print(self.clients_names)
                return {RESPONSE: 200}
            elif message[ACTION] == MESSAGE:
                return message
        return {
            RESPONSE_DEFAULT_IP_ADDRESS: 400,
            ERROR: 'Bad Request'
        }

    @Log()
    def listen(self):
        self.socket.bind((self.ip_address, self.port))
        self.socket.settimeout(0.5)
        self.socket.listen(MAX_CONNECTIONS)
        self.logger.info(self)

        while True:
            try:
                client, client_addr = self.socket.accept()
            except OSError:
                pass
            else:
                self.clients.append(client)
                self.logger.info(f'Client {client_addr} has connected to serer')
            w_clients = []
            r_clients = []
            errors = []

            try:
                if self.clients:
                    w_clients, r_clients, errors = select.select(self.clients, self.clients, [], 0)
            except OSError:
                pass

            if w_clients:
                for sock in w_clients:
                    try:
                        message = self.get_message(sock)
                        response = self.parse_message(message)
                        if ACTION in response:
                            self.messages.append({'client': sock, 'response': response})
                        else:
                            self.send_message(sock, response)
                    except:
                        self.logger.info(f'Client {sock.getpeername()} has disconnected from server')
                        self.clients.remove(sock)

            if self.messages and r_clients:
                for message in self.messages:
                    print(message['client'].getpeername())
                    self.send_message(message['client'], message['response'])
            self.messages.clear()
            #     message = self.messages.pop()
            #     for client in r_clients:
            #         try:
            #             self.send_message(client, message)
            #         except:
            #             self.logger.info(f'Client {client.getpeername()} disconnected from server.')
            #             client.close()
            #             self.clients.remove(client)


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
