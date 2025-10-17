from PySide6 import QtWidgets, QtCore
import database
from models import CATEGORIES

class TeamForm(QtWidgets.QDialog):
    """Typeform-style wizard for creating a new team."""
    
    team_created = QtCore.Signal()
    
    def __init__(self, competition_id, competition_categories, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Team")
        self.setModal(True)
        self.resize(600, 400)
        
        self.competition_id = competition_id
        self.competition_categories = competition_categories
        
        # Data storage
        self.data = {
            'category': '',
            'name': '',
            'members_count': 0,
            'women_count': 0,
            'children_count': 0,
            'elderly_count': 0,
            'member_names': [],
            'phone': None
        }
        
        # Track current question
        self.current_step = 0
        self.member_name_steps = []  # Steps for collecting member names
        
        # Setup UI
        self.setup_ui()
        self.show_step(0)
    
    def setup_ui(self):
        """Setup the user interface."""
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)
        
        # Question label
        self.question_label = QtWidgets.QLabel()
        self.question_label.setWordWrap(True)
        font = self.question_label.font()
        font.setPointSize(16)
        font.setBold(True)
        self.question_label.setFont(font)
        layout.addWidget(self.question_label)
        
        # Stacked widget for different input types
        self.input_stack = QtWidgets.QStackedWidget()
        layout.addWidget(self.input_stack)
        
        # Step 0: Category selection
        self.category_input = QtWidgets.QComboBox()
        self.category_input.addItems(self.competition_categories)
        self.input_stack.addWidget(self.category_input)
        
        # Step 1: Team name
        self.team_name_input = QtWidgets.QLineEdit()
        self.team_name_input.setPlaceholderText("Enter team name")
        self.input_stack.addWidget(self.team_name_input)
        
        # Step 2: Members count
        self.members_count_input = QtWidgets.QSpinBox()
        self.members_count_input.setRange(1, 50)
        self.members_count_input.setValue(1)
        self.input_stack.addWidget(self.members_count_input)
        
        # Step 3: Women count
        self.women_count_input = QtWidgets.QSpinBox()
        self.women_count_input.setRange(0, 50)
        self.women_count_input.setValue(0)
        self.input_stack.addWidget(self.women_count_input)
        
        # Step 4: Children count
        self.children_count_input = QtWidgets.QSpinBox()
        self.children_count_input.setRange(0, 50)
        self.children_count_input.setValue(0)
        self.input_stack.addWidget(self.children_count_input)
        
        # Step 5: Elderly count (conditional)
        self.elderly_count_input = QtWidgets.QSpinBox()
        self.elderly_count_input.setRange(0, 50)
        self.elderly_count_input.setValue(0)
        self.input_stack.addWidget(self.elderly_count_input)
        
        # Steps 6+: Member names (created dynamically)
        self.member_name_inputs = []
        
        # Last step: Phone (conditional)
        self.phone_input = QtWidgets.QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number")
        self.input_stack.addWidget(self.phone_input)
        
        # Spacer
        layout.addStretch()
        
        # Navigation buttons
        button_layout = QtWidgets.QHBoxLayout()
        
        self.back_button = QtWidgets.QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        button_layout.addWidget(self.back_button)
        
        button_layout.addStretch()
        
        self.next_button = QtWidgets.QPushButton("Next")
        self.next_button.clicked.connect(self.go_next)
        self.next_button.setDefault(True)
        button_layout.addWidget(self.next_button)
        
        layout.addLayout(button_layout)
    
    def show_step(self, step):
        """Display the specified step."""
        self.current_step = step
        
        if step == 0:
            self.question_label.setText("Select team category")
            self.input_stack.setCurrentWidget(self.category_input)
            self.back_button.setEnabled(False)
            self.next_button.setText("Next")
            
        elif step == 1:
            self.question_label.setText("What is the team name?")
            self.input_stack.setCurrentWidget(self.team_name_input)
            self.back_button.setEnabled(True)
            self.next_button.setText("Next")
            
        elif step == 2:
            self.question_label.setText("How many members are on the team?")
            self.input_stack.setCurrentWidget(self.members_count_input)
            self.back_button.setEnabled(True)
            self.next_button.setText("Next")
            
        elif step == 3:
            self.question_label.setText("How many women are on the team?")
            self.input_stack.setCurrentWidget(self.women_count_input)
            self.women_count_input.setMaximum(self.data['members_count'])
            self.back_button.setEnabled(True)
            self.next_button.setText("Next")
            
        elif step == 4:
            self.question_label.setText("How many children are on the team?")
            self.input_stack.setCurrentWidget(self.children_count_input)
            self.children_count_input.setMaximum(self.data['members_count'])
            self.back_button.setEnabled(True)
            self.next_button.setText("Next")
            
        elif step == 5:
            # Elderly count (only for categories D, E, F, O)
            if self.data['category'] in ['D', 'E', 'F', 'O']:
                self.question_label.setText("How many elderly are on the team?")
                self.input_stack.setCurrentWidget(self.elderly_count_input)
                self.elderly_count_input.setMaximum(self.data['members_count'])
                self.back_button.setEnabled(True)
                self.next_button.setText("Next")
            else:
                # Skip this step
                self.data['elderly_count'] = 0
                self.show_step(6)
                return
                
        elif step >= 6:
            # Member names
            member_index = step - 6
            if member_index < self.data['members_count']:
                # Create or get input widget
                if member_index >= len(self.member_name_inputs):
                    name_input = QtWidgets.QLineEdit()
                    name_input.setPlaceholderText("Enter member name")
                    self.member_name_inputs.append(name_input)
                    self.input_stack.addWidget(name_input)
                
                if member_index == 0:
                    self.question_label.setText("Enter the team leader's name")
                else:
                    self.question_label.setText(f"Enter member #{member_index + 1}'s name")
                
                self.input_stack.setCurrentWidget(self.member_name_inputs[member_index])
                self.back_button.setEnabled(True)
                
                # Check if this is the last member
                if member_index == self.data['members_count'] - 1:
                    # Check if phone is needed
                    if self.data['category'] in ['A', 'B']:
                        self.next_button.setText("Next")
                    else:
                        self.next_button.setText("Create Team")
                else:
                    self.next_button.setText("Next")
            else:
                # Phone number step (only for A and B)
                if self.data['category'] in ['A', 'B']:
                    self.question_label.setText("Enter phone number (optional)")
                    self.input_stack.setCurrentWidget(self.phone_input)
                    self.back_button.setEnabled(True)
                    self.next_button.setText("Create Team")
    
    def go_back(self):
        """Go to the previous step."""
        if self.current_step > 0:
            # Handle skipped elderly step
            if self.current_step == 6 and self.data['category'] not in ['D', 'E', 'F', 'O']:
                self.show_step(4)
            else:
                self.show_step(self.current_step - 1)
    
    def go_next(self):
        """Go to the next step or save."""
        if self.current_step == 0:
            # Save category
            self.data['category'] = self.category_input.currentText()
            self.show_step(1)
            
        elif self.current_step == 1:
            # Save team name
            name = self.team_name_input.text().strip()
            if not name:
                QtWidgets.QMessageBox.warning(self, "Input Required", 
                                             "Please enter a team name.")
                return
            self.data['name'] = name
            self.show_step(2)
            
        elif self.current_step == 2:
            # Save members count
            self.data['members_count'] = self.members_count_input.value()
            self.show_step(3)
            
        elif self.current_step == 3:
            # Save women count
            women_count = self.women_count_input.value()
            if women_count > self.data['members_count']:
                QtWidgets.QMessageBox.warning(self, "Invalid Input", 
                                             "Women count cannot exceed total members.")
                return
            self.data['women_count'] = women_count
            self.show_step(4)
            
        elif self.current_step == 4:
            # Save children count
            children_count = self.children_count_input.value()
            if children_count > self.data['members_count']:
                QtWidgets.QMessageBox.warning(self, "Invalid Input", 
                                             "Children count cannot exceed total members.")
                return
            self.data['children_count'] = children_count
            self.show_step(5)
            
        elif self.current_step == 5:
            # Save elderly count (if applicable)
            if self.data['category'] in ['D', 'E', 'F', 'O']:
                elderly_count = self.elderly_count_input.value()
                if elderly_count > self.data['members_count']:
                    QtWidgets.QMessageBox.warning(self, "Invalid Input", 
                                                 "Elderly count cannot exceed total members.")
                    return
                self.data['elderly_count'] = elderly_count
            self.show_step(6)
            
        elif self.current_step >= 6:
            # Save member names
            member_index = self.current_step - 6
            if member_index < self.data['members_count']:
                name = self.member_name_inputs[member_index].text().strip()
                if not name:
                    QtWidgets.QMessageBox.warning(self, "Input Required", 
                                                 "Please enter a member name.")
                    return
                
                # Store the name
                if member_index >= len(self.data['member_names']):
                    self.data['member_names'].append(name)
                else:
                    self.data['member_names'][member_index] = name
                
                # First member is the leader
                if member_index == 0:
                    self.data['leader_name'] = name
                
                # Check if there are more members
                if member_index < self.data['members_count'] - 1:
                    self.show_step(self.current_step + 1)
                else:
                    # Check if phone is needed
                    if self.data['category'] in ['A', 'B']:
                        self.show_step(self.current_step + 1)
                    else:
                        # All done, save to database
                        self.save_team()
            else:
                # Phone number step
                phone = self.phone_input.text().strip()
                if phone:
                    self.data['phone'] = phone
                # All done, save to database
                self.save_team()
    
    def save_team(self):
        """Save the team to the database."""
        try:
            team_id = database.insert_team(
                self.competition_id,
                self.data['category'],
                self.data['name'],
                self.data['members_count'],
                self.data['women_count'],
                self.data['children_count'],
                self.data['elderly_count'],
                self.data['leader_name'],
                self.data['member_names'],
                self.data['phone']
            )
            
            QtWidgets.QMessageBox.information(self, "Success", 
                                             "Team created successfully!")
            
            self.team_created.emit()
            self.accept()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", 
                                          f"Failed to create team: {str(e)}")
