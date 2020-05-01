from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib
matplotlib.use('Qt5Agg')
matplotlib.pyplot.rcParams['axes.facecolor'] = 'None'


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.set_tight_layout(True)
        self.fig.patch.set_facecolor("None")

        super(MplCanvas, self).__init__(self.fig)

        self.setStyleSheet("background-color:transparent;")
        self.axes = self.fig.add_subplot(111)

    def plot(self, x, y, x_label, y_label):
        self.clear()
        self.axes.plot(x, y)
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(y_label)
        self.draw()

    def clear(self):
        self.axes.cla()
