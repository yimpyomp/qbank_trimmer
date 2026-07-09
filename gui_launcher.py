from PySide6.QtWidgets import QApplication
from qbank_trimmer.gui.main_window import MainWindow

app = QApplication([])

window = MainWindow()
window.show()

app.exec()