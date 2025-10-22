from PySide6 import QtWidgets
import sys
from main_window import MainWindow
import logic

def run_app():
  app = QtWidgets.QApplication(sys.argv)

  app.setApplicationName("Orienteering Tables")
  app.setOrganizationName("thezanrutar")
  
  app.setStyleSheet("""
  """)

  window = MainWindow()
  window.show()

  sys.exit(app.exec())
