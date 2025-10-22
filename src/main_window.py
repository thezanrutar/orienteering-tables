from PySide6 import QtWidgets, QtCore, QtGui

class CompetitionTile(QWidgets.QFrame):
    clicked = QtCore.Signal(int) # emits competition ID
    def __init__(self, competition=None, is_add_button=False, parent=None):
        super().__init__(parent)
        self.competition = competition
        self.is_add_button = is_add_button

        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setLineWidth(1)
        self.setMinimumSize(200, 100)
        self.setCursor(QtCore.Qt.PointingHandCursor)

        # style:
        if is_add_button:
            self.setStyleSheet("""
            """)
        else:
            self.setStyleSheet("""
            """)

        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        if self.is_add_button:
            plus_label = QtWidgets.QLabel("+")
            plus_font = plus_label.fon()
            plus_font.setPointSize(48)
            plus_font.setWeight(QtGui.QFont.Light)
            plus_label.setFont(plus_font)
            plus.label.setAlignment(QtCore.Qt.AlignCenter)
            plus.label.setStyleSheet("color: rgba(255, 255, 255, 0.6);")
            layout.addWidget(plus_label)

            text_label = QtWidgets.QLabel("New Competition")
            text_label.setAlignment(QtCore.Qt.AlignCenter)
            text_label.setStyleSheet("""
                color: rgba(255, 255, 255, 0.7); font-size: 13px;
            """)
            layout.addWidget(text_label)
        else:
            date_label = QtWidgets.QLabel(self.competition['date'])
            date_font = date_label.font()
            date_font.setPointSize(14)
            date_font.setBold(True)
            date_label.setFont(date_font)
            date_label.setStyleSheet("color: #64b4ff;")
            layout.addWidget(date_label)

            location_label = QtWidgets.QLabel(self.competition['location'])
            location_label.setWordWrap(True)
            location_label.setStyleSheet("""
                color: #e8eef5; font-size: 13px; margin-top: 5px;
            """)
            layout.addWidget(location_label)
    def left_click_event(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.is_add_button:
                self.clicked.emit(-1)
            else:
                self.clicked.emit(self.competition['id'])

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Orienteering Tables")
        self.resize(900, 600)

        











