import socket
import sys
import json

from utils.constants import DEFAULT_PORT, MAX_CONNECTIONS
from utils.message import get_message


class Server:
    def __init__(self, ip_address='', port=DEFAULT_PORT):
        self.ip_address = ip_address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __str__(self):
        return f'Server is running on port {self.port}'

    def listen(self):
        self.socket.bind((self.ip_address, self.port))
        self.socket.listen(MAX_CONNECTIONS)
        print(self)

        while True:
            client, client_addr = self.socket.accept()
            try:
                message = get_message(client)
                print(message)
            except (ValueError, json.JSONDecodeError):
                print('Bad request from client')
            finally:
                client.close()


if __name__ == '__main__':
    server = Server()
    server.listen()
