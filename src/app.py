from PySide6 import QtWidgets
import sys
from main_window import MainWindow

def run_app():
    """Run the orienteering tables application."""
    app = QtWidgets.QApplication(sys.argv)
    
    # Set application info
    app.setApplicationName("Orienteering Tables")
    app.setOrganizationName("Orienteering")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())