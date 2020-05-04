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
            print('Failed to create socket. Aborting.')
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


class Udp_Client():

    def __init__(self, host='localhost', port=8010):
        try:
            self.host = socket.gethostbyname(host)
            self.port = port
        except socket.gaierror:
            print('Hostname could not be resolved. Aborting.')

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print('Failed to create socket. Aborting.')

    def send(self, message):
        bytes_to_send = str.encode(message)
        bytes_sent = self.socket.sendto(bytes_to_send, (self.host, self.port))
        if bytes_sent != len(bytes_to_send):
            print("A problem occured during sending...")
        else:
            print("Message sent!")

    def receive(self, size):
        msgFromServer = self.socket.recvfrom(size)
        msg = "Message from Server {}".format(msgFromServer[0])
        print(msg)

    def close(self):
        self.socket.close()
