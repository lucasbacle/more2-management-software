import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtCore, QtGui, QtWidgets
from networking import is_ipv4_addr, is_port
matplotlib.use('Qt5Agg')
matplotlib.pyplot.rcParams['axes.facecolor'] = 'None'


class STM_box(QtWidgets.QGroupBox):

    # see test bench for periph dict definition
    def __init__(self, parent, periph):
        super(STM_box, self).__init__(parent)

        self.periph = periph
        self.ip_placeholder = self.periph['ip']
        self.port_placeholder = str(self.periph['port'])
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
        self.setTitle(self.periph["name"])
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
        self.periph['is_activated'] = True if val > 0 else False

    def ip_update(self):
        text = self.ip_line_edit.text()

        if text == "":
            text = self.ip_line_edit.placeholderText()
            self.ip_line_edit.setText(text)

        if is_ipv4_addr(text):
            self.ip_line_edit.setStyleSheet("color:black;")
            self.periph['ip'] = text
        else:
            self.ip_line_edit.setStyleSheet("color:red;")

    def port_update(self):
        text = self.port_line_edit.text()

        if text == "":
            text = self.port_line_edit.placeholderText()
            self.port_line_edit.setText(text)

        if is_port(text):
            self.port_line_edit.setStyleSheet("color:black;")
            self.periph['port'] = int(text)
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
