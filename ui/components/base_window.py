from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

def load_stylesheet():
    file = QFile("ui/components/styles.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    return str(file.readAll(), encoding='utf-8')


class BaseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(load_stylesheet())
        self.setWindowTitle("ZenCore")