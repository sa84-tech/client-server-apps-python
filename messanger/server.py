import socket
import sys
import logging
import time

import select
from utils.decorators import Log
from utils.constants import DEFAULT_PORT, MAX_CONNECTIONS, RESPONSE, ERROR, ACTION, USER, PRESENCE, TIME, \
    RESPONSE_DEFAULT_IP_ADDRESS, MESSAGE, SENDER, MESSAGE_TEXT, RECIPIENT, EXIT, CODE, ACCOUNT_NAME, ALERT
from utils.messaging import Messaging


class Server(Messaging):
    logger = logging.getLogger('server')
    clients = []
    clients_names = {}  # {'name1': <socket>, 'name2', <socket>}
    messages = []

    def __init__(self, ip_address='', port=DEFAULT_PORT):
        super().__init__()
        self.ip_address = ip_address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __str__(self):
        return f'Server is running on port {self.port}'

    @Log()
    def parse_message(self, message, sock):
        print('PARSE', message)
        if ACTION in message:
            if message[ACTION] == PRESENCE and TIME in message and USER in message:
                client_name = message[USER].get(ACCOUNT_NAME)
                print('PARSE. CLIENT NAME: ', client_name)
                if not client_name:
                    print('PARSE. CLIENT NAME is NONE!: ', client_name)
                    return self.create_message(400, error=f'Incorrect Account name')
                if self.clients_names.get(client_name):
                    print('PARSE. CLIENT NAME: ', client_name)
                    return self.create_message(409, client_name,
                                               error=f'Someone is already connected with the given user name')
                else:
                    print('PARSE. OK - NEW USER: ', client_name)
                    self.clients_names[(message[USER][ACCOUNT_NAME])] = sock
                    out = self.create_message(200, client_name, alert=f'You have successfully connected '
                                                                      f'to server ({self.socket.getsockname()})')
                    return out
            elif message[ACTION] == MESSAGE:
                return message
            elif message[ACTION] == EXIT:
                try:
                    self.clients_names.pop((message[SENDER]))
                except KeyError:
                    pass
                else:
                    quit_message = self.create_message(code=200)
                    quit_message[ACTION] = EXIT
                    return quit_message
        return self.create_message(error=f'Bad request', code=400)

    @Log()
    def create_message(self, code, recipient='Unknown', alert=None, error=None):
        message = {
            CODE: code,
            RECIPIENT: recipient,
        }
        if alert:
            message[ALERT] = alert
        if error:
            message[ERROR] = error

        return message

    @Log()
    def get_recipient(self, message):
        user = message[RECIPIENT]
        try:
            sock = self.clients_names[user]
        except KeyError:
            return None
        print(f'GET RECIPIENT: {user}: {sock}')
        return sock

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
                self.logger.info(f'Client {client_addr} has connected to Chat')
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
                        response = self.parse_message(message, sock)
                        print('RESPONSE: ', response)
                        if ACTION in response:
                            if response[ACTION] == MESSAGE:
                                self.messages.append({SENDER: sock, RESPONSE: response})
                            if response[ACTION] == EXIT:
                                self.clients.remove(sock)
                                self.logger.info(f'Client {sock.getpeername()} left the Chat.')
                        elif CODE in response:
                            self.send_message(sock, response)

                    except:
                        self.logger.warning(f'Client {sock.getpeername()} unexpectedly disconnected from Chat')
                        self.clients.remove(sock)

            if self.messages and r_clients:
                for message in self.messages:
                    print(message[SENDER].getpeername())
                    recipient = self.get_recipient(message[RESPONSE])
                    if recipient:
                        self.send_message(recipient, message[RESPONSE])
                    else:
                        self.send_message(message[SENDER], self.create_message(code=400, error='No such user'))
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
