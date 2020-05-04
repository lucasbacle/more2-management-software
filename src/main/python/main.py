from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from datarecovery import Data_Recovery_Controller
from testbench import Test_Bench_Controller
import sys


class Main_Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main_Window, self).__init__()

        # Load UI
        uic.loadUi(appctxt.get_resource("main_window.ui"), self)
        

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext

    # Instanciate main window
    window = Main_Window()

    # Instanciate controllers
    test_bench_controller = Test_Bench_Controller(window, appctxt)
    data_recovery_controller = Data_Recovery_Controller(window, appctxt)

    # Display splash screen
    splash = QtWidgets.QSplashScreen()
    splash.setPixmap(QtGui.QPixmap(appctxt.get_resource('splash.png')))
    splash.show()
    QtCore.QTimer.singleShot(2500, splash.close)
    QtCore.QTimer.singleShot(2550, window.show)

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
