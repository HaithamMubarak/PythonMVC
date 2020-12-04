from mvc.http.httprequest import HttpRequest
import traceback
import sys
import json
import socket
import re
from threading import Thread

class IOConnection:
    BUFF_SIZE = 1024

    def __init__(self, connection):
        self.connection = connection

    def receive(self):
        res = b''
        while True:
            part = self.connection.recv(self.BUFF_SIZE)
            res += part
            if len(part) < self.BUFF_SIZE:
                break

        return HttpRequest(str(res, 'ascii'))

    def __header(self, key, value):
        if not key.isupper() and not key.islower() and '-' not in key:
            key = re.sub('(.)([A-Z])', r"\1-\2", key)

        return '%s: %s\n' % (key, value)

    def send_json(self, data='', status='200 OK', **headers):
        if not isinstance(data, str):
            data = json.dumps(data)

        headers['Content-Type'] = 'application/json'
        self.send(data, status, **headers)

    def send(self, data='', status='200 OK', **headers):
        message = 'HTTP/1.1 %s\n' % status
        for headerName in headers:
            message += self.__header(headerName, headers[headerName])

        if len(data) > 0:
            message += self.__header('Content-Length', str(len(data)))
            message += '\n'

        self.connection.send(bytes(message + data, 'ascii'))

    def close(self):
        self.connection.close()


class SocketHandler:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.connection = None

    def __enter__(self):
        self.connection = IOConnection(self.socket)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection is not None:
            self.connection.close()


class ServerThread(Thread):

    def __init__(self, ioHandler, serverHandler):
        super().__init__()
        self.ioHandler = ioHandler
        self.serverHandler = serverHandler

    def run(self):
        with self.ioHandler as io:
            httpmessage = io.receive()
            self.serverHandler(httpmessage, io)


class TcpServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self, handler=lambda message, io: print(message)):
        server_socket = socket.socket()

        config = (self.host, self.port)
        server_socket.bind(config)
        print("Connection: " + str(config))

        server_socket.listen(5)

        while True:
            c, address = server_socket.accept()  # Establish connection with client.
            ServerThread(SocketHandler(c, address), handler).start()
