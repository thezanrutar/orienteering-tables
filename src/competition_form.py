from PySide6 import QtWidgets, QtCore, QtGui
import database
from models import CATEGORIES

class CompetitionForm(QtWidgets.QDialog):
    """Typeform-style wizard for creating a new competition."""
    
    competition_created = QtCore.Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Competition")
        self.setModal(True)
        self.resize(600, 400)
        
        # Data storage
        self.data = {
            'date': '',
            'location': '',
            'categories': [],
            'ideal_times': {}
        }
        
        # Track current question
        self.current_step = 0
        self.category_time_steps = []  # Will store steps for each category time
        
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
        
        # Step 0: Date input
        self.date_input = QtWidgets.QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QtCore.QDate.currentDate())
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.input_stack.addWidget(self.date_input)
        
        # Step 1: Location input
        self.location_input = QtWidgets.QLineEdit()
        self.location_input.setPlaceholderText("e.g., Oslo, Norway")
        self.input_stack.addWidget(self.location_input)
        
        # Step 2: Categories selection
        self.categories_widget = QtWidgets.QWidget()
        categories_layout = QtWidgets.QVBoxLayout(self.categories_widget)
        self.category_checkboxes = {}
        for cat in CATEGORIES:
            checkbox = QtWidgets.QCheckBox(f"Category {cat}")
            self.category_checkboxes[cat] = checkbox
            categories_layout.addWidget(checkbox)
        categories_layout.addStretch()
        self.input_stack.addWidget(self.categories_widget)
        
        # Steps 3+: Ideal times (created dynamically)
        self.ideal_time_inputs = {}
        
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
            self.question_label.setText("When is the competition?")
            self.input_stack.setCurrentWidget(self.date_input)
            self.back_button.setEnabled(False)
            self.next_button.setText("Next")
            
        elif step == 1:
            self.question_label.setText("Where is the competition?")
            self.input_stack.setCurrentWidget(self.location_input)
            self.back_button.setEnabled(True)
            self.next_button.setText("Next")
            
        elif step == 2:
            self.question_label.setText("Select competition categories")
            self.input_stack.setCurrentWidget(self.categories_widget)
            self.back_button.setEnabled(True)
            self.next_button.setText("Next")
            
        elif step >= 3:
            # Ideal time questions for each selected category
            cat_index = step - 3
            if cat_index < len(self.data['categories']):
                category = self.data['categories'][cat_index]
                self.question_label.setText(f"What is the ideal time (minutes) for category {category}?")
                
                # Create or get the input widget for this category
                if category not in self.ideal_time_inputs:
                    time_input = QtWidgets.QSpinBox()
                    time_input.setRange(1, 999)
                    time_input.setValue(45)
                    time_input.setSuffix(" minutes")
                    self.ideal_time_inputs[category] = time_input
                    self.input_stack.addWidget(time_input)
                
                self.input_stack.setCurrentWidget(self.ideal_time_inputs[category])
                self.back_button.setEnabled(True)
                
                # Check if this is the last category
                if cat_index == len(self.data['categories']) - 1:
                    self.next_button.setText("Create Competition")
                else:
                    self.next_button.setText("Next")
    
    def go_back(self):
        """Go to the previous step."""
        if self.current_step > 0:
            self.show_step(self.current_step - 1)
    
    def go_next(self):
        """Go to the next step or save."""
        if self.current_step == 0:
            # Save date
            self.data['date'] = self.date_input.date().toString("yyyy-MM-dd")
            self.show_step(1)
            
        elif self.current_step == 1:
            # Save location
            location = self.location_input.text().strip()
            if not location:
                QtWidgets.QMessageBox.warning(self, "Input Required", 
                                             "Please enter a location.")
                return
            self.data['location'] = location
            self.show_step(2)
            
        elif self.current_step == 2:
            # Save categories
            selected_cats = [cat for cat, checkbox in self.category_checkboxes.items() 
                           if checkbox.isChecked()]
            if not selected_cats:
                QtWidgets.QMessageBox.warning(self, "Selection Required", 
                                             "Please select at least one category.")
                return
            self.data['categories'] = selected_cats
            self.show_step(3)
            
        elif self.current_step >= 3:
            # Save ideal time for current category
            cat_index = self.current_step - 3
            if cat_index < len(self.data['categories']):
                category = self.data['categories'][cat_index]
                time_value = self.ideal_time_inputs[category].value()
                self.data['ideal_times'][category] = time_value
                
                # Check if there are more categories
                if cat_index < len(self.data['categories']) - 1:
                    self.show_step(self.current_step + 1)
                else:
                    # All done, save to database
                    self.save_competition()
    
    def save_competition(self):
        """Save the competition to the database."""
        try:
            competition_id = database.insert_competition(
                self.data['date'],
                self.data['location'],
                self.data['categories'],
                self.data['ideal_times']
            )
            
            QtWidgets.QMessageBox.information(self, "Success", 
                                             "Competition created successfully!")
            
            self.competition_created.emit()
            self.accept()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", 
                                          f"Failed to create competition: {str(e)}")
