from PySide6 import QtWidgets, QtCore, QtGui
import database
from team_form import TeamForm

class Dashboard(QtWidgets.QWidget):
    """Dashboard showing competition details and teams."""
    
    back_clicked = QtCore.Signal()
    
    def __init__(self, competition_id, parent=None):
        super().__init__(parent)
        self.competition_id = competition_id
        self.competition = None
        self.teams = []
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Setup the user interface."""
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header with back button
        header_layout = QtWidgets.QHBoxLayout()
        
        back_button = QtWidgets.QPushButton("← Back")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 8px 16px;
                color: #e8eef5;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(100, 180, 255, 0.5);
            }
        """)
        back_button.clicked.connect(self.back_clicked.emit)
        header_layout.addWidget(back_button)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Competition title with icon
        self.title_label = QtWidgets.QLabel()
        title_font = self.title_label.font()
        title_font.setPointSize(24)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #64b4ff; margin-top: 10px;")
        layout.addWidget(self.title_label)
        
        # Competition details in a frosty card
        details_card = QtWidgets.QFrame()
        details_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.12),
                    stop:1 rgba(255, 255, 255, 0.08));
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        details_layout = QtWidgets.QVBoxLayout(details_card)
        
        self.details_label = QtWidgets.QLabel()
        self.details_label.setWordWrap(True)
        self.details_label.setStyleSheet("color: #e8eef5; font-size: 13px; line-height: 1.6;")
        details_layout.addWidget(self.details_label)
        
        layout.addWidget(details_card)
        
        # Teams section header
        teams_header_layout = QtWidgets.QHBoxLayout()
        teams_header_layout.setContentsMargins(0, 10, 0, 0)
        
        teams_label = QtWidgets.QLabel("👥 Teams")
        teams_font = teams_label.font()
        teams_font.setPointSize(18)
        teams_font.setBold(True)
        teams_label.setFont(teams_font)
        teams_label.setStyleSheet("color: #e8eef5;")
        teams_header_layout.addWidget(teams_label)
        
        teams_header_layout.addStretch()
        
        add_team_button = QtWidgets.QPushButton("+ Add Team")
        add_team_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(100, 180, 255, 0.3),
                    stop:1 rgba(100, 180, 255, 0.2));
                border: 1px solid rgba(100, 180, 255, 0.5);
                border-radius: 8px;
                padding: 10px 20px;
                color: #e8eef5;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(100, 180, 255, 0.4),
                    stop:1 rgba(100, 180, 255, 0.3));
            }
        """)
        add_team_button.clicked.connect(self.add_team)
        teams_header_layout.addWidget(add_team_button)
        
        layout.addLayout(teams_header_layout)
        
        # Teams table with modern styling
        self.teams_table = QtWidgets.QTableWidget()
        self.teams_table.setColumnCount(4)
        self.teams_table.setHorizontalHeaderLabels(["Team Name", "Category", "Members", "Leader"])
        self.teams_table.horizontalHeader().setStretchLastSection(True)
        self.teams_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.teams_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.teams_table.setAlternatingRowColors(True)
        self.teams_table.setStyleSheet("""
            QTableWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.08),
                    stop:1 rgba(255, 255, 255, 0.05));
                alternate-background-color: rgba(255, 255, 255, 0.1);
                gridline-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                color: #e8eef5;
            }
            QTableWidget::item {
                padding: 12px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: rgba(100, 180, 255, 0.3);
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.1));
                color: #e8eef5;
                padding: 12px;
                border: none;
                border-bottom: 2px solid rgba(100, 180, 255, 0.3);
                font-weight: 600;
                font-size: 13px;
            }
        """)
        layout.addWidget(self.teams_table)
    
    def load_data(self):
        """Load competition and team data from database."""
        # Load competition
        self.competition = database.get_competition_by_id(self.competition_id)
        if not self.competition:
            QtWidgets.QMessageBox.critical(self, "Error", "Competition not found!")
            return
        
        # Update UI with competition info
        self.title_label.setText(f"{self.competition['location']}")
        
        # Format ideal times
        ideal_times_str = ", ".join([f"{cat}: {time}m" 
                                    for cat, time in self.competition['ideal_times'].items()])
        
        details = f"""
<b>Date:</b> {self.competition['date']}<br>
<b>Categories:</b> {', '.join(self.competition['categories'])}<br>
<b>Ideal Times:</b> {ideal_times_str}
        """.strip()
        
        self.details_label.setText(details)
        
        # Load teams
        self.refresh_teams()
    
    def refresh_teams(self):
        """Refresh the teams table."""
        self.teams = database.get_teams_by_competition(self.competition_id)
        
        self.teams_table.setRowCount(len(self.teams))
        
        for i, team in enumerate(self.teams):
            # Team name
            name_item = QtWidgets.QTableWidgetItem(team['name'])
            self.teams_table.setItem(i, 0, name_item)
            
            # Category
            category_item = QtWidgets.QTableWidgetItem(team['category'])
            self.teams_table.setItem(i, 1, category_item)
            
            # Members count
            members_text = f"{team['members_count']} ({team['women_count']}W, {team['children_count']}C"
            if team['elderly_count'] > 0:
                members_text += f", {team['elderly_count']}E"
            members_text += ")"
            members_item = QtWidgets.QTableWidgetItem(members_text)
            self.teams_table.setItem(i, 2, members_item)
            
            # Leader
            leader_item = QtWidgets.QTableWidgetItem(team['leader_name'])
            self.teams_table.setItem(i, 3, leader_item)
        
        # Resize columns to content
        self.teams_table.resizeColumnsToContents()
    
    def add_team(self):
        """Open the add team dialog."""
        form = TeamForm(self.competition_id, self.competition['categories'], self)
        form.team_created.connect(self.refresh_teams)
        form.exec()
