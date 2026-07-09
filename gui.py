from qbank_trimmer.catalog import load_skill_catalog, get_learning_areas, get_skills
from PySide6.QtWidgets import (QApplication,
                               QWidget,
                               QMainWindow,
                               QLabel,
                               QPushButton,
                               QVBoxLayout,
                               QSpinBox,
                               QHBoxLayout,
                               QRadioButton,
                               QGroupBox,
                               QCheckBox,
                               QComboBox)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.layout = None
        self.central_widget = None
        self.title = None
        self.button = None
        self.question_count = None

        # Setup for having skills in dropdowns
        self.skill_catalog = {}

        self.setWindowTitle("SAT Question Generator")

        self.setup_ui()
        self.setup_connections()




    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.build_title()
        self.build_subject_group()

        self.build_learning_area_selector()
        # self.update_learning_areas()

        self.build_skill_selector()

        self.build_difficulty_group()
        self.build_question_selector()

        # Keep this as the last thing
        self.build_generate_button()

        self.update_skill_catalog()


    def build_title(self):
        self.title = QLabel("SAT Question Generator")
        self.layout.addWidget(self.title)

    def build_subject_group(self):
        # Create subject groups
        self.subject_group = QGroupBox("Subject")

        # Create subject buttons
        self.rw_button = QRadioButton("Reading and Writing")
        self.math_button = QRadioButton("Math")

        # Selecting RW by default
        self.rw_button.setChecked(True)

        # Horizontal row
        subject_layout = QHBoxLayout()

        # Add subject group
        self.subject_group.setLayout(subject_layout)
        subject_layout.addWidget(self.rw_button)
        subject_layout.addWidget(self.math_button)

        self.layout.addWidget(self.subject_group)


    def build_difficulty_group(self):
        # Create difficulty group
        self.difficulty_group = QGroupBox("Difficulty")

        # Buttons for each
        self.easy_button = QCheckBox("Easy")
        self.medium_button = QCheckBox("Medium")
        self.hard_button = QCheckBox("Hard")

        self.easy_button.setChecked(True)

        difficulty_layout = QHBoxLayout()

        self.difficulty_group.setLayout(difficulty_layout)
        difficulty_layout.addWidget(self.easy_button)
        difficulty_layout.addWidget(self.medium_button)
        difficulty_layout.addWidget(self.hard_button)

        self.layout.addWidget(self.difficulty_group)

    def build_question_selector(self):
        self.layout.addWidget(QLabel("Number of Questions"))

        self.question_count = QSpinBox()
        self.question_count.setRange(1, 100)
        self.question_count.setValue(20)

        self.layout.addWidget(self.question_count)

    def build_generate_button(self):
        self.button = QPushButton("Generate")
        self.layout.addWidget(self.button)

    def build_learning_area_selector(self):
        self.learning_area_label = QLabel("Learning Area")

        # Setting up the dropdown
        self.learning_area = QComboBox()

        self.layout.addWidget(self.learning_area_label)
        self.layout.addWidget(self.learning_area)

    def build_skill_selector(self):
        self.skill_dropdown_label = QLabel("Skill")

        self.skill_dropdown = QComboBox()

        self.layout.addWidget(self.skill_dropdown_label)
        self.layout.addWidget(self.skill_dropdown)

    def setup_connections(self):
        # Generate button
        self.button.clicked.connect(self.button_clicked)

        # Learning area dropdown
        # self.rw_button.clicked.connect(self.update_learning_areas)
        self.rw_button.clicked.connect(self.update_skill_catalog)
        # self.math_button.toggled.connect(self.update_learning_areas)
        self.math_button.clicked.connect(self.update_skill_catalog)

        self.learning_area.currentTextChanged.connect(self.update_skills)


    def update_learning_areas(self):
        if self.rw_button.isChecked():
            subject = "rw"
        else:
            subject = "math"

        self.skill_catalog = load_skill_catalog(subject)
        self.learning_area.clear()
        self.learning_area.addItems(self.skill_catalog.keys())

    def update_skill_catalog(self):
        if self.math_button.isChecked():
            subject = "math"
        else:
            subject = "rw"

        self.skill_catalog = load_skill_catalog(subject)

        self.learning_area.clear()
        self.learning_area.addItems(self.skill_catalog.keys())
        self.update_skills()

    def update_skills(self):
        learning_area = self.learning_area.currentText()

        skills = self.skill_catalog.get(learning_area, [])

        self.skill_dropdown.clear()

        # Adding option for no skills
        self.skill_dropdown.addItem("All Skills")
        self.skill_dropdown.addItems(skills)

    def get_difficulties(self):
        difficulties = []

        if self.easy_button.isChecked():
            difficulties.append("Easy")

        if self.medium_button.isChecked():
            difficulties.append("Medium")

        if self.hard_button.isChecked():
            difficulties.append("Hard")

        return difficulties


    def get_settings(self):
        difficulties = self.get_difficulties()

        question_count = self.question_count.value()

        skill = self.skill_dropdown.currentText()
        if skill == "All Skills":
            skill = None

        return {"subject": "math" if self.math_button.isChecked() else "rw",
                "difficulty": difficulties,
                "learning_area": self.learning_area.currentText(),
                "skill": skill,
                "count": question_count}


    def button_clicked(self):
        settings = self.get_settings()
        print(settings)




app = QApplication([])

window = MainWindow()
window.show()

app.exec()