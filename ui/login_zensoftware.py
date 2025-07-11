from ui.components.base_window import BaseWindow
from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton

class LoginWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.title = QLabel("Iniciar sesión en ZenCore")
        self.title.setObjectName("title")

        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Correo")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Contraseña")
        self.input_password.setEchoMode(QLineEdit.Password)

        self.button_login = QPushButton("Ingresar")

        layout.addWidget(self.title)
        layout.addWidget(self.input_user)
        layout.addWidget(self.input_password)
        layout.addWidget(self.button_login)