from PySide6 import QtWidgets
import sys
from main_window import MainWindow

def run_app():
    """Run the orienteering tables application."""
    app = QtWidgets.QApplication(sys.argv)
    
    # Set application info
    app.setApplicationName("Orienteering Tables")
    app.setOrganizationName("Orienteering")
    
    # Apply modern dark theme stylesheet
    app.setStyleSheet("""
        /* Main application background */
        QMainWindow, QWidget {
            background-color: #0f1a2e;
            color: #e8eef5;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        /* Scroll areas */
        QScrollArea {
            background-color: transparent;
            border: none;
        }
        
        /* Labels */
        QLabel {
            color: #e8eef5;
            background-color: transparent;
        }
        
        /* Buttons */
        QPushButton {
            background-color: rgba(255, 255, 255, 0.1);
            color: #e8eef5;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 500;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 0.05);
        }
        
        /* Line edits and inputs */
        QLineEdit, QSpinBox, QComboBox, QDateEdit {
            background-color: rgba(255, 255, 255, 0.08);
            color: #e8eef5;
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 6px;
            padding: 8px 12px;
            min-height: 25px;
        }
        
        QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QDateEdit:focus {
            border: 1px solid rgba(100, 180, 255, 0.6);
            background-color: rgba(255, 255, 255, 0.12);
        }
        
        /* Combo box dropdown */
        QComboBox::drop-down {
            border: none;
            width: 30px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #e8eef5;
            margin-right: 10px;
        }
        
        QComboBox QAbstractItemView {
            background-color: #1a2a45;
            color: #e8eef5;
            border: 1px solid rgba(255, 255, 255, 0.2);
            selection-background-color: rgba(100, 180, 255, 0.3);
        }
        
        /* Checkboxes */
        QCheckBox {
            color: #e8eef5;
            spacing: 8px;
        }
        
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
            border-radius: 4px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            background-color: rgba(255, 255, 255, 0.08);
        }
        
        QCheckBox::indicator:checked {
            background-color: rgba(100, 180, 255, 0.5);
            border: 1px solid rgba(100, 180, 255, 0.8);
        }
        
        /* Table widget */
        QTableWidget {
            background-color: rgba(255, 255, 255, 0.05);
            alternate-background-color: rgba(255, 255, 255, 0.08);
            gridline-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            color: #e8eef5;
        }
        
        QTableWidget::item {
            padding: 8px;
            border: none;
        }
        
        QTableWidget::item:selected {
            background-color: rgba(100, 180, 255, 0.3);
        }
        
        QHeaderView::section {
            background-color: rgba(255, 255, 255, 0.1);
            color: #e8eef5;
            padding: 8px;
            border: none;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            font-weight: 600;
        }
        
        /* Dialogs */
        QDialog {
            background-color: #0f1a2e;
        }
        
        /* Message boxes */
        QMessageBox {
            background-color: #0f1a2e;
        }
        
        QMessageBox QLabel {
            color: #e8eef5;
        }
        
        /* Separators */
        QFrame[frameShape="4"] {
            color: rgba(255, 255, 255, 0.2);
        }
        
        /* Calendar widget */
        QCalendarWidget {
            background-color: #1a2a45;
        }
        
        QCalendarWidget QWidget {
            color: #e8eef5;
        }
        
        QCalendarWidget QAbstractItemView {
            background-color: #1a2a45;
            selection-background-color: rgba(100, 180, 255, 0.3);
        }
    """)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())