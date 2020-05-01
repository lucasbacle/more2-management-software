import socket
import data_generator

TCP_IP = '127.0.0.1'
TCP_PORT = 9000
BUFFER_SIZE = 20

FRAME_LENGTH = 184  # bits


def eeprom_init():
    return data_generator.generate_data(1200) # mission will length 1200 sec = 20 minutes at most


def eeprom_clear(eeprom_size):
    eeprom = ""
    for i in range(0, eeprom_size):
        eeprom += "11111111"
    return eeprom


def wrap_length_prefix(message):
    message_length = len(message)
    result = bytes([message_length])
    result += message
    return result


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    while (1):
        memory = eeprom_init()

        conn, addr = s.accept()
        print("Connection address:", addr)

        finish = False
        while not finish:

            try:
                data = conn.recv(BUFFER_SIZE)
                data = data.decode("utf-8").split()
                # print(data)

                if len(data) > 0:
                    if data[0] == "clear":
                        memory = eeprom_clear(len(memory))

                    elif data[0] == "readall":

                        for i in range(0, int(len(memory)/FRAME_LENGTH)):
                            message = memory[(i*FRAME_LENGTH):FRAME_LENGTH*(i+1)]
                            message = int(message, 2).to_bytes(len(message) // 8, byteorder='big')
                            message = wrap_length_prefix(message)
                            conn.sendall(message)

                        message = bytes("OK", encoding="utf-8")
                        message = wrap_length_prefix(message)
                        conn.sendall(message)

            except Exception as exc:
                print("ERROR: ", exc)
                finish = True
                conn.close()
                print("Goodbye!")

    s.shutdown(socket.SHUT_RDWR)
    s.close()
