# ui/splash_screen.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer
from utils.verificacion import verificar_entorno

class SplashVentana(QWidget):
    def __init__(self, callback_login, callback_bienvenida):
        super().__init__()
        self.setWindowTitle("Verificando entorno - ZenCore")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()
        self.status_label = QLabel("Verificando conexión...")
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        self.callback_login = callback_login
        self.callback_bienvenida = callback_bienvenida

        QTimer.singleShot(1000, self.verificar_entorno)

    def verificar_entorno(self):
        estado = verificar_entorno()
        self.status_label.setText(estado["mensaje"])

        QTimer.singleShot(1500, lambda: self.enrutar(estado["ruta"]))

    def enrutar(self, destino):
        self.close()
        if destino == "login":
            self.callback_login()
        elif destino == "bienvenida":
            self.callback_bienvenida()