from PySide6.QtWidgets import QApplication
import sys

from ui.splash_screen import SplashVentana
from ui.login_zensoftware import LoginWindow

def mostrar_login():
    login = LoginWindow()
    login.show()

def mostrar_bienvenida():
    print("Mostrar pantalla de bienvenida o crear cuenta")  # Aquí irá el flujo de creación

if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash = SplashVentana(callback_login=mostrar_login, callback_bienvenida=mostrar_bienvenida)
    splash.show()

    sys.exit(app.exec())