import matplotlib
from networking import Tcp_Client, ServerDisconnectedError, is_ipv4_addr, is_port
from pandas import DataFrame, ExcelWriter, concat
from PyQt5 import QtWidgets, QtCore


# USER CONSTANTS
# (data name, size in bits)
# It is assumed that there is one timestamp per data coming before it
FRAME_DEFINITION = [("temperature", 12),
                    ("pressure", 12),
                    ("acceleration", 16),
                    ("payload", 16)]

TIMESTAMP_SIZE = 32  # in bits

# APP CONSTANTS (do not touch)
FRAME_LENGTH = 0
for elem in FRAME_DEFINITION:
    FRAME_LENGTH += elem[1] + TIMESTAMP_SIZE  # in bit

FRAME_SIZE = FRAME_LENGTH // 8  # in byte

SUCCESS = True
FAILURE = False


class DataNotLockedError(Exception):
    pass


class Data():

    def __init__(self, name, units):
        self.data = {'time': [], 'value': []}
        self.units = units
        self.name = name
        self.is_locked = False

    def lock(self):
        self.is_locked = True
        self.data = DataFrame(self.data)

    def add(self, timestamp, value):
        if not self.is_locked:
            self.data['time'].append(timestamp)
            self.data['value'].append(value)

    def clear(self):
        self.data = {'time': [], 'value': []}
        self.is_locked = False

    def get_dataframe(self):
        if self.is_locked:
            return self.data.copy()
        raise DataNotLockedError


class Data_Recovery_Controller():

    def __init__(self, parent, app_context):
        # MODEL
        self.is_connected = False
        self.data = {"temperature": Data("Temperature", "°C"),
                     "pressure": Data("Pressure", "psi"),
                     "acceleration": Data("Acceleration", "G"),
                     "payload": Data("Luminosité", "%")}

        # VIEW
        self.parent = parent
        parent.get_data_button.clicked.connect(self.get_obc_data)
        parent.clear_button.clicked.connect(self.clear_obc_memory)
        parent.export_csv_button.clicked.connect(self.export_to_csv)
        parent.export_xls_button.clicked.connect(self.export_to_xls)
        parent.connection_button.clicked.connect(
            self.connection_button_pressed)
        parent.obc_ip_line_edit.editingFinished.connect(self.ip_update)
        parent.obc_port_line_edit.editingFinished.connect(self.port_update)
        parent.data_combo.currentIndexChanged.connect(
            self.data_selection_changed)

    def ip_update(self):
        text = self.parent.obc_ip_line_edit.text()

        if text == "":
            self.parent.obc_ip_line_edit.setText(
                self.parent.obc_ip_line_edit.placeholderText())

        if text == "" or is_ipv4_addr(text):
            self.parent.obc_ip_line_edit.setStyleSheet("color:black;")
        else:
            self.parent.obc_ip_line_edit.setStyleSheet("color:red;")

    def port_update(self):
        text = self.parent.obc_port_line_edit.text()

        if text == "":
            self.parent.obc_port_line_edit.setText(
                self.parent.obc_port_line_edit.placeholderText())

        if text == "" or is_port(text):
            self.parent.obc_port_line_edit.setStyleSheet("color:black;")
        else:
            self.parent.obc_port_line_edit.setStyleSheet("color:red;")

    def data_selection_changed(self, item_index=None):
        item = self.parent.data_combo.currentText()
        item = item.lower()
        self.plot(item)

    def plot(self, data_key):
        self.parent.plotCanvas.clear()
        self.data[data_key].get_dataframe().plot(
            'time', 'value', ax=self.parent.plotCanvas.axes, legend=False)
        self.parent.plotCanvas.axes.set_xlabel('time (s)')
        self.parent.plotCanvas.axes.set_ylabel(
            self.data[data_key].name + " (" + self.data[data_key].units + ")")
        self.parent.plotCanvas.draw()

    def connection_button_pressed(self):
        if self.is_connected:
            self.disconnect()
        else:
            self.connect()

    def connect(self):
        ip = self.parent.obc_ip_line_edit.text()
        port = int(self.parent.obc_port_line_edit.text())
        self.tcp_client = Tcp_Client(ip, port)

        self.is_connected = True

        self.parent.connection_button.setText("Disconnect")
        self.parent.operations_box.setEnabled(True)
        self.parent.obc_ip_line_edit.setEnabled(False)
        self.parent.obc_port_line_edit.setEnabled(False)

    def disconnect(self):
        self.tcp_client.close()

        self.is_connected = False

        self.parent.connection_button.setText("Connect")
        self.parent.operations_box.setEnabled(False)
        self.parent.obc_ip_line_edit.setEnabled(True)
        self.parent.obc_port_line_edit.setEnabled(True)

    def clear_obc_memory(self):
        print("Clear OBC memory")
        reply = QtWidgets.QMessageBox.question(
            self.parent, "Clear EEPROM", "Are you sure? This is definitive.", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.tcp_client.send("clear")
        else:
            print("Cancel!")

    def get_obc_data(self):
        print("# Get OBC data")
        self.tcp_client.send("readall")

        raw_data = []
        finished = False
        while not finished:
            try:
                length_prefix = self.tcp_client.receive(1)
                length_prefix = int.from_bytes(
                    length_prefix, byteorder='big', signed=False)
                message = self.tcp_client.receive(length_prefix)
                if message == b"OK":
                    finished = True
                else:
                    raw_data += message
            except ServerDisconnectedError:
                break

        if finished == True:  # have received all the data ?
            self.process_raw(raw_data)

            # Process the data and update view :
            # enable data-related view elements
            self.parent.groupBox.setEnabled(True)
            self.parent.export_box.setEnabled(True)

            # plot data
            # TODO: select first element in the combo
            self.plot("temperature")

    def process_raw(self, raw_data):
        # TODO: stop using strings, work directly with bytes...
        # TODO: make this function frame size independant...

        # Unlock and clear previous data
        for key in self.data:
            self.data[key].clear()

        for i in range(0, int(len(raw_data)/FRAME_SIZE)):
            frame = raw_data[i*FRAME_SIZE:(i+1)*FRAME_SIZE]
            frame = bytes(frame)
            frame = f"{int.from_bytes(frame,'big'):0184b}"  # TODO: NOT GOOD

            # Translate the frame to understandable data
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

                self.data[elem_type].add(time, value)

        # lock data to allow export
        for key in self.data:
            self.data[key].lock()

    def export_to_csv(self):
        print("Export to .csv file")
        path = QtWidgets.QFileDialog.getSaveFileName(
            self.parent, "Save data", None, "CSV files (*.csv)")

        if len(path) > 0:
            # Clean file extension
            file_info = QtCore.QFileInfo(path[0])
            path = file_info.absolutePath() + '/' + file_info.baseName()

            df_list = []
            for key in self.data:
                dataframe = self.data[key].get_dataframe()
                dataframe.columns = ['time', key] # rename 'value' -> key
                df_list.append(dataframe)

            with open(path+'.csv', 'w') as f:
                concat(df_list, axis=1).to_csv(f)

    def export_to_xls(self):
        print("Export to .xls file")
        path = QtWidgets.QFileDialog.getSaveFileName(
            self.parent, "Save data", None, "XLS files (*.xls)")

        if len(path) > 0:
            # Clean file extension
            file_info = QtCore.QFileInfo(path[0])
            path = file_info.absolutePath() + '/' + file_info.baseName()
            print(path)
            with ExcelWriter(path+'.xls') as writer:  # pylint: disable=abstract-class-instantiated
                for key in self.data:
                    self.data[key].get_dataframe().to_excel(
                        writer, sheet_name=key)
