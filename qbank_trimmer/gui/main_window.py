from qbank_trimmer.catalog import load_skill_catalog, lookup_id, load_catalog
from qbank_trimmer.gui.worker import GenerationWorker
from qbank_trimmer.config import GENERATED_DIR
from PySide6.QtWidgets import (QWidget,
                               QMainWindow,
                               QLabel,
                               QPushButton,
                               QVBoxLayout,
                               QSpinBox,
                               QHBoxLayout,
                               QRadioButton,
                               QGroupBox,
                               QCheckBox,
                               QComboBox,
                               QMessageBox,
                               QFileDialog,
                               QTabWidget,
                               QLineEdit)
from PySide6.QtCore import QThread
from pathlib import Path

from qbank_trimmer.utils import create_output_directory


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

        self.question_catalogs = {}

        # Initializing output folder, none = default location
        self.output_directory = None

        self.setWindowTitle("SAT Question Generator")

        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.build_title()

        # Adding new code for tabs
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.build_generate_tab()
        self.build_lookup_tab()

        self.build_status_label()   # shared, sits below the tabs

        self.update_skill_catalog()

    def build_generate_tab(self):
        generate_tab = QWidget()
        self.generate_layout = QVBoxLayout()
        generate_tab.setLayout(self.generate_layout)

        self.build_subject_group()
        self.build_learning_area_selector()
        self.build_skill_selector()
        self.build_difficulty_group()
        self.build_question_selector()
        self.build_output_selector()
        self.build_generate_button()

        self.tabs.addTab(generate_tab, "Generate Questions")

    def build_lookup_tab(self):
        lookup_tab = QWidget()
        self.lookup_layout = QVBoxLayout()
        lookup_tab.setLayout(self.lookup_layout)

        # Add subject selector
        self.lookup_subject_group = QGroupBox("Subject")
        self.lookup_math_button = QRadioButton("Math")
        self.lookup_rw_button = QRadioButton("Reading and Writing")
        self.lookup_rw_button.setChecked(True)

        lookup_subject_layout = QHBoxLayout()
        self.lookup_subject_group.setLayout(lookup_subject_layout)
        lookup_subject_layout.addWidget(self.lookup_rw_button)
        lookup_subject_layout.addWidget(self.lookup_math_button)


        self.lookup_layout.addWidget(self.lookup_subject_group)

        self.lookup_layout.addWidget(QLabel("Look Up Answer by Question ID"))

        self.lookup_input = QLineEdit()
        self.lookup_input.setPlaceholderText("Enter question ID...")
        self.lookup_layout.addWidget(self.lookup_input)

        self.lookup_button = QPushButton("Look Up")
        self.lookup_layout.addWidget(self.lookup_button)

        self.lookup_result = QLabel("")
        self.lookup_layout.addWidget(self.lookup_result)

        self.tabs.addTab(lookup_tab, "Answer Lookup")

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

        self.generate_layout.addWidget(self.subject_group)

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

        self.generate_layout.addWidget(self.difficulty_group)

    def build_question_selector(self):
        self.layout.addWidget(QLabel("Number of Questions"))

        self.question_count = QSpinBox()
        self.question_count.setRange(1, 100)
        self.question_count.setValue(20)

        self.generate_layout.addWidget(self.question_count)

    def build_generate_button(self):
        self.button = QPushButton("Generate")
        self.generate_layout.addWidget(self.button)

    def build_status_label(self):
        self.status_label = QLabel("Ready")
        self.layout.addWidget(self.status_label)

    def build_learning_area_selector(self):
        self.learning_area_label = QLabel("Learning Area")

        # Setting up the dropdown
        self.learning_area = QComboBox()

        self.generate_layout.addWidget(self.learning_area_label)
        self.generate_layout.addWidget(self.learning_area)

    def build_skill_selector(self):
        self.skill_dropdown_label = QLabel("Skill")

        self.skill_dropdown = QComboBox()

        self.generate_layout.addWidget(self.skill_dropdown_label)
        self.generate_layout.addWidget(self.skill_dropdown)

    def build_output_selector(self):
        self.output_label = QLabel("Output Folder")

        self.output_path = QLabel("Default")

        self.output_button = QPushButton("Browse")

        self.generate_layout.addWidget(self.output_label)
        self.generate_layout.addWidget(self.output_path)
        self.generate_layout.addWidget(self.output_button)

    def choose_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder: ")

        if folder:
            self.output_directory = Path(folder)
            self.output_path.setText(folder)

    def setup_connections(self):
        # Generate button
        self.button.clicked.connect(self.button_clicked)

        # Learning area dropdown
        # self.rw_button.clicked.connect(self.update_learning_areas)
        self.rw_button.clicked.connect(self.update_skill_catalog)
        # self.math_button.toggled.connect(self.update_learning_areas)
        self.math_button.clicked.connect(self.update_skill_catalog)

        self.learning_area.currentTextChanged.connect(self.update_skills)

        self.output_button.clicked.connect(self.choose_output_folder)

        self.lookup_button.clicked.connect(self.handle_lookup)

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

    def update_question_catalog(self):
        subject = "math" if self.lookup_math_button.isChecked() else "rw"
        self.question_catalog = load_catalog(subject)


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
            difficulties.append("easy")

        if self.medium_button.isChecked():
            difficulties.append("medium")

        if self.hard_button.isChecked():
            difficulties.append("hard")

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
                "count": question_count,
                "catalog_path": None,
                "questions_output_path": self.output_directory / "selected_questions.pdf",
                "answers_output_path": self.output_directory / "selected_answers.pdf"}

    def start_generation(self):
        self.output_directory = create_output_directory(GENERATED_DIR)
        settings = self.get_settings()

        self.generation_started()

        self.thread = QThread()
        self.worker = GenerationWorker(settings)

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)

        self.worker.progress.connect(self.update_status)

        self.worker.finished.connect(self.generation_finished)
        self.worker.error.connect(self.generation_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)

        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.worker.deleteLater)

        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def button_clicked(self):
        try:
            self.start_generation()

        except Exception as e:
            self.generation_error(e)

    def generation_finished(self):
        self.status_label.setText("Done!")
        self.button.setEnabled(True)

    def generation_error(self, message):
        self.button.setEnabled(True)
        self.status_label.setText("Generation failed")

        QMessageBox.critical(self, "Generation Error", message)

    def generation_started(self):
        self.status_label.setText("Generating questions...")
        self.button.setEnabled(False)

    def update_status(self, message):
        self.status_label.setText(message)

    def handle_lookup(self):
        question_id = self.lookup_input.text().strip()

        if not question_id:
            self.lookup_result.setText("Enter a question ID first.")
            return

        subject = "math" if self.lookup_math_button.isChecked() else "rw"
        catalog = self.get_question_catalog(subject)

        try:
            results = lookup_id(catalog, question_id)
            self.lookup_result.setText(f"Answer: {results['answer']}\n"
                                       f"Key Page: {results['key_page']}\n"
                                       f"Blank Page: {results['blank_page']}")
        except ValueError as e:
            self.lookup_result.setText(str(e))

    def get_question_catalog(self, subject):
        if subject not in self.question_catalogs.keys():
            self.question_catalogs[subject] = load_catalog(subject)

        return self.question_catalogs[subject]
