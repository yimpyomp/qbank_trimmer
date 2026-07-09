from PySide6.QtCore import QObject, Signal
from qbank_trimmer.app import generate_questions

class GenerationWorker(QObject):
    finished = Signal()
    error = Signal(str)

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    def run(self):
        try:
            generate_questions(self.settings)
            self.finished.emit()

        except Exception as e:
            self.error.emit(str(e))