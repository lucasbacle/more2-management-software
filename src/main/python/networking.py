import socket
import sys


def is_ipv4_addr(ip_str):
    try:
        socket.inet_aton(ip_str)
        return True
    except socket.error:
        return False


def is_port(port_str):
    try:
        port = int(port_str)
        if 0 <= port <= 65535:
            return True
    except ValueError:
        pass

    return False


class ServerDisconnectedError(Exception):

    def __init__(self):
        self.message = "Server has closed connection"


class Tcp_Client():

    def __init__(self, host='localhost', port=8010):
        self.host = host
        self.port = port

        try:
            # create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # resolve hostname
            remote_ip = socket.gethostbyname(self.host)
            # connect to server
            self.socket.connect((remote_ip, self.port))
            print('# Connected to server : ' +
                  self.host + ' (' + remote_ip + ')')
        except socket.error:
            print('Failed to create socket')
        except socket.gaierror:
            print('Hostname could not be resolved. Aborting')

    def send(self, request):
        try:
            print('# Sending data to server')
            self.socket.sendall(bytes(request, encoding="utf-8"))
        except socket.error:
            print('Send failed')

    def receive(self, size):
        data = self.socket.recv(size)
        if len(data) > 0:
            return data
        else:
            self.close()
            raise ServerDisconnectedError

    def close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
