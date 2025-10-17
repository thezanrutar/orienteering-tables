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
        
        # Set style
        if is_add_button:
            self.setStyleSheet("""
                CompetitionTile {
                    background-color: #f0f0f0;
                    border: 2px dashed #999;
                    border-radius: 5px;
                }
                CompetitionTile:hover {
                    background-color: #e0e0e0;
                    border: 2px dashed #666;
                }
            """)
        else:
            self.setStyleSheet("""
                CompetitionTile {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                CompetitionTile:hover {
                    background-color: #f9f9f9;
                    border: 2px solid #666;
                }
            """)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the tile UI."""
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        if self.is_add_button:
            # Add button tile
            plus_label = QtWidgets.QLabel("+")
            plus_font = plus_label.font()
            plus_font.setPointSize(48)
            plus_label.setFont(plus_font)
            plus_label.setAlignment(QtCore.Qt.AlignCenter)
            plus_label.setStyleSheet("color: #999;")
            layout.addWidget(plus_label)
            
            text_label = QtWidgets.QLabel("New Competition")
            text_label.setAlignment(QtCore.Qt.AlignCenter)
            text_label.setStyleSheet("color: #666;")
            layout.addWidget(text_label)
        else:
            # Competition tile
            date_label = QtWidgets.QLabel(self.competition['date'])
            date_font = date_label.font()
            date_font.setPointSize(12)
            date_font.setBold(True)
            date_label.setFont(date_font)
            layout.addWidget(date_label)
            
            location_label = QtWidgets.QLabel(self.competition['location'])
            location_label.setWordWrap(True)
            layout.addWidget(location_label)
            
            layout.addStretch()
            
            # Team count
            team_count = database.get_team_count_by_competition(self.competition['id'])
            teams_label = QtWidgets.QLabel(f"{team_count} teams")
            teams_label.setStyleSheet("color: #666;")
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
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QtWidgets.QLabel("Orienteering Competitions")
        title_font = title.font()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Scroll area for competition grid
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        layout.addWidget(scroll)
        
        # Competition grid container
        self.grid_container = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(15)
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