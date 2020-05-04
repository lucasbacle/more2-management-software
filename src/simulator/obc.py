from threading import Thread
import data_generator
import socket


IP = "127.0.0.1"
PORT = 9000
BUFFER_SIZE = 20
FRAME_LENGTH = 184  # in bits


class Memory():

    # mission will length 1200 sec = 20 minutes at most
    def __init__(self, duration=1200):
        self.init(duration)

    def init(self, duration):
        self.content = data_generator.generate_data(duration)

    def clear(self):
        content = ""
        for _ in range(0, len(self.content)):
            content += "1"
        self.content = content

    def read(self, start, stop):
        return self.content[start:stop]

    def get_size(self):
        return len(self.content)


class Client_Thread(Thread):

    def __init__(self, socket, memory):
        Thread.__init__(self)
        self.socket = socket
        self.memory = memory

    def _wrap_length_prefix(self, message):
        message_length = len(message)
        result = bytes([message_length])
        result += message
        return result

    def send(self, message):
        message = self._wrap_length_prefix(message)
        self.socket.sendall(message)

    def run(self):
        finish = False
        while not finish:
            try:
                data = self.socket.recv(BUFFER_SIZE)

                if len(data) > 0:
                    data = data.decode("utf-8").split()

                    if data[0] == "clear":
                        self.memory.clear()

                    elif data[0] == "readall":
                        # Send all the relevant data
                        frame_number = self.memory.get_size() // FRAME_LENGTH
                        for i in range(0, frame_number):
                            message = self.memory.read(i*FRAME_LENGTH,
                                                       FRAME_LENGTH*(i+1))
                            message = int(message, 2).to_bytes(len(message) // 8,
                                                               byteorder='big')
                            self.send(message)

                        # Say that the transfer is now done
                        message = bytes("OK", encoding="utf-8")
                        self.send(message)
                else:
                    finish = True
                    print("OBC > Goodbye!")

            except Exception as exc:
                finish = True
                print("OBC > ERROR: ", exc)

        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()


class On_Board_Computer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.active_threads = []
        # initialize memory content
        self.memory = Memory()
        print("OBC > memory content size :", self.memory.get_size(), "bits")
        # create an INET, STREAMing socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        self.socket.bind((IP, PORT))
        print("OBC > server up and listening (", IP, ":", PORT, ")")
        # become a server socket, expect 1 client awaiting connection at most
        self.socket.listen(1)

    def run(self):
        while True:
            # accept connections from outside
            (clientsocket, address) = self.socket.accept()
            print("OBC > new connection :", address)
            # now do something with the clientsocket
            ct = Client_Thread(clientsocket, self.memory)
            self.active_threads.append(ct)
            ct.start()

        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
