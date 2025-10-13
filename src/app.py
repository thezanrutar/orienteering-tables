from PySide6 import QtWidgets
import sys
import main_window

def run_app():
  app = QtWidgets.QApplication(sys.argv)
  window = main_window.MainWindow()
  window.show()
  app.exec()