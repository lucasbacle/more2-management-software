import socket
from threading import Thread

IP = "localhost"
PORT = 8003
BUFFER_SIZE = 1024


class Stm_Uart(Thread):

    def __init__(self):
        Thread.__init__(self)

        # Create a datagram socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind to address and ip
        self.socket.bind((IP, PORT))

        print("UART > server up and listening (", IP, ":", PORT, ")")

    def run(self):
        # Listen for incoming datagrams
        while True:
            message, address = self.socket.recvfrom(BUFFER_SIZE)
            message = message.decode('utf-8')
            print("UART > Message from", address, ":", message)
