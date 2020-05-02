from PyQt5 import QtWidgets


class Test_Bench_Controller():

    def __init__(self, parent):
        self.parent = parent

    def load(self):
        dlg = QtWidgets.QFileDialog(self.parent)
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        if dlg.exec_():
            print(dlg.selectedFiles())
            # TODO: load config from file

    def save(self):
        paths = QtWidgets.QFileDialog.getSaveFileName(self.parent, "Save configuration", None, "JSON files (*.json)")
        print(paths)
        # TODO: save config to file

    def start_test(self):
        print("Clear OBC memory")
        reply = QtWidgets.QMessageBox.question(
            self.parent, "Start test", "Are you ready to begin?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            pass
        else:
            print("Cancel!")

        # TODO: prepare testing
        # TODO: launch testing
        # TODO: monitor tests
