from PyQt5 import QtWidgets, uic
from widgets import STM_box
from networking import Udp_Client


class Test_Bench_Controller():

    def __init__(self, parent, app_context):
        # Model
        self.ethernet = {"name": "Ethernet",
                         "ip": "localhost",
                         "port": 8001,
                         "is_activated": False,
                         "ui_filename": "configure_ethernet_widget.ui"}
        self.spi = {"name": "SPI",
                    "ip": "localhost",
                    "port": 8002,
                    "is_activated": False,
                    "ui_filename": "configure_spi_widget.ui"}
        self.uart = {"name": "UART",
                     "ip": "localhost",
                     "port": 8003,
                     "is_activated": False,
                     "ui_filename": "configure_uart_widget.ui"}
        self.model = [self.ethernet, self.spi, self.uart]

        # View
        self.parent = parent
        # Populate the test windows
        for periph in self.model:
            # Add the stm boxes
            w = STM_box(parent.tab_test, periph)
            parent.verticalLayout_7.addWidget(w)

            # Add the page
            page = uic.loadUi(app_context.get_resource(periph['ui_filename']))
            parent.configure_stackedwidget.addWidget(page)

            # Add corresponding item to the combo box
            parent.bus_combobox.addItem(periph['name'])

        # Signals
        parent.load_button.clicked.connect(self.load)
        parent.save_button.clicked.connect(self.save)
        parent.start_button.clicked.connect(self.start_test)

    def load(self):
        dlg = QtWidgets.QFileDialog(self.parent)
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        if dlg.exec_():
            print(dlg.selectedFiles())
            # TODO: load config from file

    def save(self):
        paths = QtWidgets.QFileDialog.getSaveFileName(
            self.parent, "Save configuration", None, "JSON files (*.json)")
        print(paths)
        # TODO: save config to file

    def start_test(self):
        reply = QtWidgets.QMessageBox.question(
            self.parent, "Start test", "Are you ready to begin?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            # TODO: prepare tests & then monitor them

            # launch testing
            for test_item in self.model:

                if test_item['is_activated']:
                    ip = test_item['ip']
                    port = test_item['port']
                    udp_client = Udp_Client(ip, port)
                    message = "Hello, " + test_item['name'] + "!"
                    udp_client.send(message)
                    udp_client.close()

        else:
            print("Cancel!")
