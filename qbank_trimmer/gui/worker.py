from PySide6.QtCore import QObject
from qbank_trimmer.app import generate_questions

class GenerationWorker(QObject):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    def run(self):
        generate_questions(self.settings)