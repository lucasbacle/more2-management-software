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
        uic.loadUi(appctxt.get_resource("main_window.ui"), self)
        #self.ui.setupUi(self)

        # Populate the test windows
        for periph in self.data:
            # Add the stm boxes
            w = STM_box(self.tab_test,
                        title=periph["name"],
                        ip=periph["ip"],
                        port=periph["port"])
            self.verticalLayout_7.addWidget(w)

            # Add the page
            page = uic.loadUi(appctxt.get_resource(periph['ui_filename']))
            self.configure_stackedwidget.addWidget(page)

            # Add corresponding item to the combo box
            self.bus_combobox.addItem(periph['name'])

        # Instanciate controllers
        self.test_bench_controller = Test_Bench_Controller(self)
        self.data_recovery_controller = Data_Recovery_Controller(self)

        # Signals
        self.load_button.clicked.connect(self.test_bench_controller.load)
        self.save_button.clicked.connect(self.test_bench_controller.save)
        self.start_button.clicked.connect(self.test_bench_controller.start_test)
        

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
