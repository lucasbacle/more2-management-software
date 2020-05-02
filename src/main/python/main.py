from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets, QtGui, QtCore, uic

from mydesign import Ui_MainWindow  # importing our generated file
from widgets import STM_box
from datarecovery import Data_Recovery_Controller
from testbench import Test_Bench_Controller
from networking import Tcp_Client
import sys


class mywindow(QtWidgets.QMainWindow):

    def __init__(self):

        super(mywindow, self).__init__()

        # Test bench data
        self.ethernet = {"name": "Ethernet",
                         "ip": "192.168.0.1",
                         "port": "8000",
                         "isActivated": False,
                         "ui_filename": "configure_ethernet_widget.ui"}
        self.spi = {"name": "SPI",
                    "ip": "192.168.0.2",
                    "port": "8000",
                    "isActivated": False,
                    "ui_filename": "configure_spi_widget.ui"}
        self.uart = {"name": "UART",
                     "ip": "192.168.0.3",
                     "port": "8000",
                     "isActivated": False,
                     "ui_filename": "configure_uart_widget.ui"}
        self.data = [self.ethernet, self.spi, self.uart]

        # Load UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Populate the test windows
        for periph in self.data:
            # Add the stm boxes
            w = STM_box(self.ui.tab_test,
                        title=periph["name"],
                        ip=periph["ip"],
                        port=periph["port"])
            self.ui.verticalLayout_7.addWidget(w)

            # Add the page
            page = uic.loadUi(appctxt.get_resource(periph['ui_filename']))
            self.ui.configure_stackedwidget.addWidget(page)

            # Add corresponding item to the combo box
            self.ui.bus_combobox.addItem(periph['name'])

        # Prepare connectivity

        # Instanciate controllers
        self.test_bench_controller = Test_Bench_Controller(self)
        self.data_recovery_controller = Data_Recovery_Controller(self)

        # Signals
        self.ui.load_button.clicked.connect(self.test_bench_controller.load)
        self.ui.save_button.clicked.connect(self.test_bench_controller.save)
        self.ui.start_button.clicked.connect(
            self.test_bench_controller.start_test)
        self.ui.get_data_button.clicked.connect(
            self.data_recovery_controller.get_obc_data)
        self.ui.clear_button.clicked.connect(
            self.data_recovery_controller.clear_obc_memory)
        self.ui.export_csv_button.clicked.connect(
            self.data_recovery_controller.export_to_csv)
        self.ui.export_xls_button.clicked.connect(
            self.data_recovery_controller.export_to_xls)
        self.ui.connection_button.clicked.connect(
            self.data_recovery_controller.connection_button_pressed)
        
        self.ui.obc_ip_line_edit.editingFinished.connect(self.data_recovery_controller.ip_update)
        self.ui.obc_port_line_edit.editingFinished.connect(self.data_recovery_controller.port_update)
        
        self.ui.data_combo.currentIndexChanged.connect(self.data_recovery_controller.data_selection_changed)

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = mywindow()

    splash = QtWidgets.QSplashScreen()
    splash.setPixmap(QtGui.QPixmap(appctxt.get_resource('splash.png')))
    splash.show()

    QtCore.QTimer.singleShot(2500, splash.close)
    QtCore.QTimer.singleShot(2550, window.show)

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
