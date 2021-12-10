import socket
import sys
import json
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
        # print('SERVER parse message', message)
        if ACTION in message:
            if message[ACTION] == PRESENCE and TIME in message and ACCOUNT_NAME in message:
                return {RESPONSE: 200}
            elif message[ACTION] == MESSAGE:
                return {
                    ACTION: MESSAGE,
                    SENDER: message.get(ACCOUNT_NAME),
                    TIME: time.time(),
                    MESSAGE_TEXT: message[MESSAGE_TEXT].upper()
                }
        return {
            RESPONSE_DEFAULT_IP_ADDRESS: 400,
            ERROR: 'Bad Request'
        }

    @Log()
    def listen(self):
        self.socket.bind((self.ip_address, self.port))
        self.socket.listen(MAX_CONNECTIONS)
        self.socket.settimeout(1)
        self.logger.info(self)

        while True:
            try:
                client, client_addr = self.socket.accept()
            except OSError:
                pass
            else:
                self.clients.append(client)
                self.logger.info(f'Client {client_addr} has connected to server')
            # print('self.clients', self.clients)
            w_clients = []
            r_clients = []
            errors = []

            try:
                if self.clients:
                    w_clients, r_clients, errors = select.select(self.clients, self.clients, [], 0)
            except OSError:
                pass

            # print('w_clients, r_clients', w_clients, r_clients)

            if w_clients:
                for sock in w_clients:
                    try:
                        message = self.get_message(sock)
                        response = self.parse_message(message)
                        print('RESPONSE', response)
                        # self.send_message(sock, response)
                        if ACTION in response:
                            self.messages.append(response)
                        else:
                            self.send_message(sock, response)
                    except:
                        self.logger.error(f'Bad request from client: {sock.getpeername()}')
                        self.clients.remove(sock)
                    # finally:
                    #     sock.close()
                    # self.send_message(sock, response)

            if self.messages and r_clients:
                # message = {
                #     ACTION: MESSAGE,
                #     SENDER: messages[0][0],
                #     TIME: time.time(),
                #     MESSAGE_TEXT: messages[0][1]
                # }
                # del messages[0]
                message = self.messages.pop()
                print('POP1(message)', message, '\nPOP2(messages)', self.messages)
                for client in r_clients:
                    try:
                        self.send_message(client, message)
                    except:
                        self.logger.info(f'Client {client.getpeername()} disconnected from server.')
                        self.clients.remove(client)



            # except (ValueError, json.JSONDecodeError):
            #     self.logger.error(f'Bad request from client: {client}')
            # finally:
            #     client.close()


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
