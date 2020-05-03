import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtCore, QtGui, QtWidgets
from networking import is_ipv4_addr, is_port
matplotlib.use('Qt5Agg')
matplotlib.pyplot.rcParams['axes.facecolor'] = 'None'


class STM_box(QtWidgets.QGroupBox):

    def __init__(self, parent=None, title="peripheral", ip="192.168.0.0", port="8000"):
        super(STM_box, self).__init__(parent)

        self.ip_placeholder = ip
        self.port_placeholder = port
        self.ip = self.ip_placeholder
        self.port = self.port_placeholder
        self.is_activated = False

        # create UI :
        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        # IP field
        self.ip_layout = QtWidgets.QHBoxLayout()
        self.ip_label = QtWidgets.QLabel(self)
        self.ip_layout.addWidget(self.ip_label)
        self.ip_line_edit = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.ip_line_edit.setSizePolicy(sizePolicy)
        self.ip_layout.addWidget(self.ip_line_edit)
        self.verticalLayout.addLayout(self.ip_layout)

        # Port field
        self.port_layout = QtWidgets.QHBoxLayout()
        self.port_label = QtWidgets.QLabel(self)
        self.port_layout.addWidget(self.port_label)
        self.port_line_edit = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Fixed)
        self.port_line_edit.setSizePolicy(sizePolicy)
        self.port_layout.addWidget(self.port_line_edit)
        self.verticalLayout.addLayout(self.port_layout)

        # Activate checkbox
        self.activate_checkbox = QtWidgets.QCheckBox(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.activate_checkbox.setSizePolicy(sizePolicy)
        self.verticalLayout.addWidget(self.activate_checkbox)

        # Add text
        self.setTitle(title)
        self.ip_label.setText("IP :")
        self.ip_line_edit.setPlaceholderText(self.ip_placeholder)
        self.port_label.setText("Port :")
        self.port_line_edit.setPlaceholderText(self.port_placeholder)
        self.activate_checkbox.setText("Activate")

        # Signals
        self.activate_checkbox.stateChanged.connect(self.activate_update)
        self.ip_line_edit.editingFinished.connect(self.ip_update)
        self.port_line_edit.editingFinished.connect(self.port_update)

    def activate_update(self, val):
        self.is_activated = val

    def ip_update(self):
        text = self.ip_line_edit.text()

        if text == "":
            self.ip_line_edit.setText(self.ip_line_edit.placeholderText())

        if text == "" or is_ipv4_addr(text):
            self.ip_line_edit.setStyleSheet("color:black;")
        else:
            self.ip_line_edit.setStyleSheet("color:red;")

    def port_update(self):
        text = self.port_line_edit.text()

        if text == "":
            self.port_line_edit.setText(
                self.port_line_edit.placeholderText())

        if text == "" or is_port(text):
            self.port_line_edit.setStyleSheet("color:black;")
        else:
            self.port_line_edit.setStyleSheet("color:red;")


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.set_tight_layout(True)
        self.fig.patch.set_facecolor("None")

        super(MplCanvas, self).__init__(self.fig)

        self.setStyleSheet("background-color:transparent;")
        self.axes = self.fig.add_subplot(111)

    def clear(self):
        self.axes.cla()
