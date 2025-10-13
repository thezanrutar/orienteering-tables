from PySide6 import QtWidgets, QtCore

class MainWindow(QtWidgets.QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Orienteering Tables")