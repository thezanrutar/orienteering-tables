from PySide6 import QtWidgets, QtCore, QtGui
import database
from competition_form import CompetitionForm
from dashboard import Dashboard

class CompetitionTile(QtWidgets.QFrame):
    """Tile widget for displaying a competition."""
    
    clicked = QtCore.Signal(int)  # Emits competition ID
    
    def __init__(self, competition=None, is_add_button=False, parent=None):
        super().__init__(parent)
        self.competition = competition
        self.is_add_button = is_add_button
        
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setLineWidth(1)
        self.setMinimumSize(200, 150)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        
        # Set style with frosty glass effect
        if is_add_button:
            self.setStyleSheet("""
                CompetitionTile {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 255, 255, 0.12),
                        stop:1 rgba(255, 255, 255, 0.08));
                    border: 2px dashed rgba(255, 255, 255, 0.3);
                    border-radius: 12px;
                }
                CompetitionTile:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 255, 255, 0.18),
                        stop:1 rgba(255, 255, 255, 0.12));
                    border: 2px dashed rgba(100, 180, 255, 0.5);
                }
            """)
        else:
            self.setStyleSheet("""
                CompetitionTile {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 255, 255, 0.15),
                        stop:1 rgba(255, 255, 255, 0.1));
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 12px;
                }
                CompetitionTile:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(255, 255, 255, 0.2),
                        stop:1 rgba(255, 255, 255, 0.15));
                    border: 1px solid rgba(100, 180, 255, 0.5);
                }
            """)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the tile UI."""
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        if self.is_add_button:
            # Add button tile with icon
            plus_label = QtWidgets.QLabel("+")
            plus_font = plus_label.font()
            plus_font.setPointSize(48)
            plus_font.setWeight(QtGui.QFont.Light)
            plus_label.setFont(plus_font)
            plus_label.setAlignment(QtCore.Qt.AlignCenter)
            plus_label.setStyleSheet("color: rgba(255, 255, 255, 0.6);")
            layout.addWidget(plus_label)
            
            text_label = QtWidgets.QLabel("New Competition")
            text_label.setAlignment(QtCore.Qt.AlignCenter)
            text_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 13px;")
            layout.addWidget(text_label)
        else:
            # Competition tile with modern styling
            date_label = QtWidgets.QLabel(self.competition['date'])
            date_font = date_label.font()
            date_font.setPointSize(14)
            date_font.setBold(True)
            date_label.setFont(date_font)
            date_label.setStyleSheet("color: #64b4ff;")
            layout.addWidget(date_label)
            
            location_label = QtWidgets.QLabel(self.competition['location'])
            location_label.setWordWrap(True)
            location_label.setStyleSheet("color: #e8eef5; font-size: 13px; margin-top: 5px;")
            layout.addWidget(location_label)
            
            layout.addStretch()
            
            # Team count with icon
            team_count = database.get_team_count_by_competition(self.competition['id'])
            teams_label = QtWidgets.QLabel(f"👥 {team_count} teams")
            teams_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 12px;")
            layout.addWidget(teams_label)
    
    def mousePressEvent(self, event):
        """Handle mouse press."""
        if event.button() == QtCore.Qt.LeftButton:
            if self.is_add_button:
                self.clicked.emit(-1)
            else:
                self.clicked.emit(self.competition['id'])

class MainWindow(QtWidgets.QMainWindow):
    """Main application window showing competition grid."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Orienteering Tables")
        self.resize(900, 600)
        
        # Initialize database
        database.init_db()
        
        # Create central widget with stacked layout
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.stacked_layout = QtWidgets.QStackedLayout(self.central_widget)
        
        # Main page (competition grid)
        self.main_page = QtWidgets.QWidget()
        self.setup_main_page()
        self.stacked_layout.addWidget(self.main_page)
        
        # Load competitions
        self.refresh_competitions()
    
    def setup_main_page(self):
        """Setup the main competition grid page."""
        layout = QtWidgets.QVBoxLayout(self.main_page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title with modern styling
        title = QtWidgets.QLabel("🏃 Orienteering Competitions")
        title_font = title.font()
        title_font.setPointSize(28)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #e8eef5; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Scroll area for competition grid
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        layout.addWidget(scroll)
        
        # Competition grid container
        self.grid_container = QtWidgets.QWidget()
        self.grid_container.setStyleSheet("background-color: transparent;")
        self.grid_layout = QtWidgets.QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(20)
        scroll.setWidget(self.grid_container)
    
    def refresh_competitions(self):
        """Refresh the competition grid."""
        # Clear existing tiles
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get competitions from database
        competitions = database.get_competitions()
        
        # Add competition tiles
        cols = 3  # Number of columns in grid
        for i, comp in enumerate(competitions):
            row = i // cols
            col = i % cols
            
            tile = CompetitionTile(comp)
            tile.clicked.connect(self.open_competition)
            self.grid_layout.addWidget(tile, row, col)
        
        # Add "+" button tile
        row = len(competitions) // cols
        col = len(competitions) % cols
        add_tile = CompetitionTile(is_add_button=True)
        add_tile.clicked.connect(self.create_competition)
        self.grid_layout.addWidget(add_tile, row, col)
        
        # Add stretch to push tiles to top
        self.grid_layout.setRowStretch(row + 1, 1)
    
    def create_competition(self, _):
        """Open the competition creation dialog."""
        form = CompetitionForm(self)
        form.competition_created.connect(self.refresh_competitions)
        form.exec()
    
    def open_competition(self, competition_id):
        """Open the competition dashboard."""
        dashboard = Dashboard(competition_id, self)
        dashboard.back_clicked.connect(lambda: self.close_dashboard(dashboard))
        self.stacked_layout.addWidget(dashboard)
        self.stacked_layout.setCurrentWidget(dashboard)
    
    def close_dashboard(self, dashboard):
        """Close the dashboard and return to main view."""
        self.stacked_layout.setCurrentWidget(self.main_page)
        self.stacked_layout.removeWidget(dashboard)
        dashboard.deleteLater()
        # Refresh in case teams were added
        self.refresh_competitions()