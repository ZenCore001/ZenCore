from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QApplication, QFrame,
    QGraphicsDropShadowEffect, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt, QTimer, QSize, QThread, Signal
from PySide6.QtGui import QPixmap, QMovie, QColor
from utils.internet_check import hay_conexion, conexion_estable
from core.terminal_checker import obtener_hardware_id, terminal_esta_registrada
from utils.servidor_check import servidor_esta_activo
import os

# ------------------------
# HILO PARA TAREAS BLOQUEANTES
# ------------------------
class PasoWorker(QThread):
    terminado = Signal(bool, str)  # (exito, mensaje)

    def __init__(self, funcion):
        super().__init__()
        self.funcion = funcion

    def run(self):
        try:
            exito, mensaje = self.funcion()
            self.terminado.emit(exito, mensaje)
        except Exception as e:
            self.terminado.emit(False, str(e))


# ------------------------
# SPLASH SCREEN
# ------------------------
class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 500)

        self.terminal_registrada = False
        self.cuenta_verificada = False

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignCenter)

        self.container = QFrame()
        self.container.setFixedSize(300, 460)
        self.container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                border: none;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.container.setGraphicsEffect(shadow)

        self.content_layout = QVBoxLayout(self.container)
        self.content_layout.setContentsMargins(25, 20, 25, 20)
        self.content_layout.setSpacing(15)
        self.content_layout.setAlignment(Qt.AlignCenter)

        logo = QLabel()
        logo_path = os.path.join("assets", "logo.png")
        logo.setPixmap(QPixmap(logo_path).scaled(130, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(logo)

        self.loader = QLabel()
        self.loader.setFixedSize(48, 48)
        self.loader.setAlignment(Qt.AlignCenter)
        self.movie = QMovie(os.path.join("assets", "loader.gif"))
        self.movie.setScaledSize(QSize(48, 48))
        self.loader.setMovie(self.movie)
        self.movie.start()
        self.content_layout.addWidget(self.loader, alignment=Qt.AlignCenter)

        self.status_label = QLabel("Iniciando...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("font-size: 14px; color: #444;")
        self.content_layout.addWidget(self.status_label)

        self.boton_layout = QHBoxLayout()
        self.boton_layout.setSpacing(10)
        self.boton_layout.setAlignment(Qt.AlignCenter)

        self.boton_salir = QPushButton("Salir")
        self.boton_salir.setFixedHeight(40)
        self.boton_salir.setStyleSheet("""
            QPushButton {
                min-width: 100px;
                background-color: #cc0000;
                color: white;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #990000; }
        """)
        self.boton_salir.clicked.connect(QApplication.instance().quit)

        self.boton_accion = QPushButton("...")
        self.boton_accion.setFixedHeight(40)
        self.boton_accion.setStyleSheet("""
            QPushButton {
                min-width: 100px;
                background-color: #007acc;
                color: white;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #005f99; }
        """)
        self.boton_accion.clicked.connect(self.accion_correspondiente)

        self.boton_layout.addWidget(self.boton_salir)
        self.boton_layout.addWidget(self.boton_accion)
        self.content_layout.addLayout(self.boton_layout)
        self.boton_salir.hide()
        self.boton_accion.hide()

        main_layout.addWidget(self.container)

        # Pasos y ejecución inicial
        self.steps = [
            ("Verificando conexión a internet...", lambda: (hay_conexion(), "Conexión detectada")),
            ("Conexión estable...", lambda: (conexion_estable(), "Conexión estable")),
            ("Conectando con el servidor Zensoftware...", lambda: (servidor_esta_activo(), "Servidor accesible")),
            ("Registrando terminal...", self.realizar_verificacion_terminal),
            ("Verificando la cuenta Zensoftware...", self.realizar_verificacion_cuenta),
            ("Actualizando las bases de datos...", self.condicional("Actualización omitida")),
            ("Mandando estatus general...", self.condicional("Estatus omitido")),
            ("Buscando actualizaciones...", self.condicional("Búsqueda omitida")),
            ("Instalando actualización...", self.condicional("Instalación omitida")),
            ("Inicializando...", self.condicional("Inicialización lista")),
        ]

        self.current_step = 0
        self.next_step()

    def condicional(self, mensaje):
        return lambda: ((self.terminal_registrada and self.cuenta_verificada), mensaje)

    def next_step(self):
        if self.current_step < len(self.steps):
            texto, funcion = self.steps[self.current_step]
            self.status_label.setText(texto)
            print(f"[DEBUG] Ejecutando paso {self.current_step + 1}: {texto}")

            self.worker = PasoWorker(funcion)
            self.worker.terminado.connect(self.step_resultado)
            self.worker.start()
        else:
            print("[DEBUG] Todos los pasos completados.")
            self.finalizar()

    def step_resultado(self, exito, mensaje):
        if exito:
            print(f"[INFO] Éxito: {mensaje}")
            self.status_label.setText(f"✔ {mensaje}")
        else:
            print(f"[ERROR] Falló: {mensaje}")
            self.status_label.setText(f"❌ {mensaje}")

        self.current_step += 1
        QTimer.singleShot(900, self.next_step)

    def realizar_verificacion_terminal(self):
        hardware_id = obtener_hardware_id()
        print(f"[DEBUG] Verificando hardware_id: {hardware_id}")
        estado = terminal_esta_registrada(hardware_id)
        self.terminal_registrada = estado
        return (estado, "Terminal reconocida" if estado else "Terminal no registrada")

    def realizar_verificacion_cuenta(self):
        if self.terminal_registrada:
            self.cuenta_verificada = True
            return (True, "Cuenta asociada verificada")
        else:
            self.cuenta_verificada = False
            return (False, "No existe una cuenta asociada")

    def finalizar(self):
        print("[DEBUG] Evaluando destino final...")
        self.loader.setVisible(False)
        self.status_label.setText("Por favor, seleccione una opción.")
        self.boton_salir.show()
        self.boton_accion.show()

        if self.terminal_registrada and self.cuenta_verificada:
            print("[DESTINO] Ir al sistema principal.")
            self.boton_accion.setText("Entrar al sistema")
        elif not self.terminal_registrada and self.cuenta_verificada:
            print("[DESTINO] Iniciar sesión para asociar terminal.")
            self.boton_accion.setText("Iniciar sesión")
        elif not self.terminal_registrada and not self.cuenta_verificada:
            print("[DESTINO] Crear nueva cuenta ZenSoftware.")
            self.boton_accion.setText("Crear cuenta")
        else:
            print("[DESTINO] Flujo indefinido.")
            self.boton_accion.setText("Reintentar")

    def accion_correspondiente(self):
        if self.terminal_registrada and self.cuenta_verificada:
            print("[UI] Abrir sistema principal")
        elif not self.terminal_registrada and self.cuenta_verificada:
            print("[UI] Abrir login")
        elif not self.terminal_registrada and not self.cuenta_verificada:
            print("[UI] Abrir formulario de creación de cuenta")
        else:
            print("[UI] Reintentar verificación")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
