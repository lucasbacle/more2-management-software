from PyQt5 import QtCore, QtWidgets
import socket


class STM_box(QtWidgets.QGroupBox):

    def __init__(self, parent=None, title="peripheral", ip="192.168.0.0", port="8000"):
        super(STM_box, self).__init__(parent)

        self.ip_placeholder = ip
        self.port_placeholder = port
        self.ip = self.ip_placeholder
        self.port = self.port_placeholder
        self.isActivated = False

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
        print("Activated!" if val else "Not activated!")
        self.isActivated = val

    def ip_update(self):
        text = self.ip_line_edit.text()
        isOk = True

        if text == "":
            self.ip = self.ip_placeholder
        else:
            try:
                socket.inet_aton(text)
                self.ip = text
                print(self.ip)
            except socket.error:
                isOk = False

        if isOk:
            self.ip_line_edit.setStyleSheet("color:black;")
        else:
            self.ip_line_edit.setStyleSheet("color:red;")

    def port_update(self):
        text = self.port_line_edit.text()
        isOk = True

        if text == "":
            self.port = self.port_placeholder
        else:
            try:
                port = int(text)
                if 0 <= port <= 65535:
                    self.port_line_edit.setStyleSheet("color:black;")
                    self.port = port
                    print(self.port)
                else:
                    isOk = False
            except ValueError:
                isOk = False

        if isOk:
            self.port_line_edit.setStyleSheet("color:black;")
        else:
            self.port_line_edit.setStyleSheet("color:red;")
