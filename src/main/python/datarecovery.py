from network import Tcp_Client, is_ipv4_addr, is_port
import binascii
import matplotlib
from PyQt5 import QtWidgets

DATA_FRAME_SIZE = int(184/8)  # in byte

FRAME_DEFINITION = [("temperature", 12),
                    ("pressure", 12),
                    ("acceleration", 16),
                    ("payload", 16)]

TIMESTAMP_SIZE = 32


class data_sample():

    def __init__(self, timestamp, value):
        self.timestamp = timestamp
        self.value = value

    def __str__(self):
        return "{ t: " + str(self.timestamp) + ", data: " + str(self.value) + " }"


class Data_Recovery_Controller():

    def __init__(self, parent):
        self.parent = parent
        self.is_connected = False
        self.data = {"temperature": [], "pressure": [],
                     "acceleration": [], "payload": []}

    def ip_update(self):
        text = self.parent.ui.obc_ip_line_edit.text()

        if text == "":
            self.parent.ui.obc_ip_line_edit.setText(
                self.parent.ui.obc_ip_line_edit.placeholderText())

        if text == "" or is_ipv4_addr(text):
            self.parent.ui.obc_ip_line_edit.setStyleSheet("color:black;")
        else:
            self.parent.ui.obc_ip_line_edit.setStyleSheet("color:red;")

    def port_update(self):
        text = self.parent.ui.obc_port_line_edit.text()

        if text == "":
            self.parent.ui.obc_port_line_edit.setText(
                self.parent.ui.obc_port_line_edit.placeholderText())

        if text == "" or is_port(text):
            self.parent.ui.obc_port_line_edit.setStyleSheet("color:black;")
        else:
            self.parent.ui.obc_port_line_edit.setStyleSheet("color:red;")

    def connection_button_pressed(self):
        if self.is_connected:
            self.disconnect()
        else:
            self.connect()

    def data_selection_changed(self, item_index=None):
        item = self.parent.ui.data_combo.currentText()
        item = item.lower()
        self.plot(item)

    def plot(self, data_name):
        time = []
        y = []

        for elem in self.data[data_name]:
            time.append(elem.timestamp)
            y.append(elem.value)

        self.parent.ui.plotCanvas.plot(time, y, "time (s)", data_name)

    # MODEL Stuff

    def connect(self):
        ip = self.parent.ui.obc_ip_line_edit.text()
        port = int(self.parent.ui.obc_port_line_edit.text())
        self.tcp_client = Tcp_Client(ip, port)

        self.is_connected = True

        self.parent.ui.connection_button.setText("Disconnect")
        self.parent.ui.operations_box.setEnabled(True)
        self.parent.ui.obc_ip_line_edit.setEnabled(False)
        self.parent.ui.obc_port_line_edit.setEnabled(False)

    def disconnect(self):
        self.tcp_client.close()

        self.is_connected = False

        self.parent.ui.connection_button.setText("Connect")
        self.parent.ui.operations_box.setEnabled(False)
        self.parent.ui.obc_ip_line_edit.setEnabled(True)
        self.parent.ui.obc_port_line_edit.setEnabled(True)

    def clear_obc_memory(self):
        print("Clear OBC memory")
        reply = QtWidgets.QMessageBox.question(
            self.parent, "Clear EEPROM", "Are you sure? This is definitive.", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.tcp_client.send("clear")
        else:
            print("Cancel!")

    def get_obc_data(self):
        # TODO: protect from infinite looping here :)

        print("# Get OBC data")
        self.tcp_client.send("readall")

        data = []

        finished = False
        while not finished:
            length_prefix = self.tcp_client.receive(1)
            length_prefix = int.from_bytes(
                length_prefix, byteorder='big', signed=False)
            message = self.tcp_client.receive(length_prefix)
            if message == b"OK":
                finished = True
            else:
                data += message

        self.data = {"temperature": [], "pressure": [],
                     "acceleration": [], "payload": []}

        # TODO: check if success
        self.process_raw(data)

        # enable data-related view elements
        self.parent.ui.groupBox.setEnabled(True)

        # plot data
        self.plot("temperature")

    def process_raw(self, data):
        print(len(data))

        for i in range(0, int(len(data)/DATA_FRAME_SIZE)):
            frame = data[i*DATA_FRAME_SIZE:(i+1)*DATA_FRAME_SIZE]
            frame = bytes(frame)
            frame = f"{int.from_bytes(frame,'big'):0184b}"

            #print("M", i, ": ", frame)

            # Convert frame to understandable data
            index = 0
            for elem in FRAME_DEFINITION:
                elem_type = elem[0]
                elem_length = elem[1]

                timestamp = frame[index:index+TIMESTAMP_SIZE]
                index += TIMESTAMP_SIZE
                value = int(frame[index:index+elem_length], base=2)
                index += elem_length

                # convert timestamp to sec
                time = int(timestamp[0:8], base=2)*60 + int(timestamp[8:16],
                                                            base=2) + (int(timestamp[16:32], base=2) / 1024.0)

                sample = data_sample(time, value)
                self.data[elem_type].append(sample)

        print("DONE!")

    def export_to_csv(self):
        print("Export to .cvs file")
        # TODO: Export to .cvs file

    def export_to_xls(self):
        print("Export to .xls file")
        # TODO: Export to .xls file