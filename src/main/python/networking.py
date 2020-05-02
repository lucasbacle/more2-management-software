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


class Tcp_Client():

    def __init__(self, host='localhost', port=8010):
        self.host = host
        self.port = port

        # create socket
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print('Failed to create socket')
            sys.exit()

        try:
            remote_ip = socket.gethostbyname(self.host)
        except socket.gaierror:
            print('Hostname could not be resolved. Exiting')
            sys.exit()

        # Connect to remote server
        print('# Connecting to server, ' + self.host + ' (' + remote_ip + ')')
        self.socket.connect((remote_ip, self.port))

    def send(self, request):
        try:
            print('# Sending data to server')
            self.socket.sendall(bytes(request, encoding="utf-8"))
        except socket.error:
            print('Send failed')
            sys.exit()

    def receive(self, size):
        data = self.socket.recv(size)
        return data

    def close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
