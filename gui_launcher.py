from PySide6.QtWidgets import QApplication, QMessageBox
from qbank_trimmer.gui.main_window import MainWindow
from qbank_trimmer.config import validate_resources

app = QApplication([])

missing = validate_resources()

if missing:
    QMessageBox.critical(None, "Missing Files",
                         "The following required files are missing:\n\n" + "\n".join(missing))

    exit(1)

window = MainWindow()
window.show()

app.exec()