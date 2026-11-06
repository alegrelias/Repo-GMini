import os
import sqlite3
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gmini.Backend.app.db.databaseService import DataBaseService
from gmini.Backend.app.services.sessionManager import SessionManager
from gmini.Frontend.login_register.register_window import Register
from gmini.Frontend.main_window.main_window import MainWindow


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.session_manager = SessionManager()
        self.db_service = DataBaseService()
        self.password_visible = False
        self.inicializacion_ui()

    def inicializacion_ui(self):
        self.setFixedSize(400, 400)
        self.setWindowTitle("GMini GUI")
        self.setStyleSheet("""
            QWidget { background-color: #2b2e33; color: white; }
            QLabel { font-size: 16px; }
            QLineEdit {
                background-color: #2b2e33; border: 1px solid #5a6b7d;
                border-radius: 10px; padding: 8px; font-size: 14px;
            }
            QPushButton {
                border: 1px solid #5a6b7d; border-radius: 10px;
                padding: 10px; font-size: 16px;
            }
            QPushButton#btnLogin {
                background-color: #2f5275; font-weight: bold;
            }
        """)

        layout = QVBoxLayout(self)
        title = QLabel("GMini                                      LEAB")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #D8DEE9;")
        layout.addWidget(title)

        self.label_error = QLabel("")
        self.label_error.setStyleSheet("color: #ff5555; font-size: 14px;")
        self.label_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_error)

        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("Usuario"))
        self.user_input = QLineEdit()
        user_layout.addWidget(self.user_input)
        layout.addLayout(user_layout)

        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("Contraseña"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        resources = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Resources"))
        self.icono_ojo_cerrado = QIcon(os.path.join(resources, "ojo_cerrado.jpg"))
        self.icono_ojo_abierto = QIcon(os.path.join(resources, "ojo_abierto.jpg"))
        self.action_ver_password = self.password_input.addAction(
            self.icono_ojo_cerrado, QLineEdit.ActionPosition.TrailingPosition
        )
        self.action_ver_password.triggered.connect(self.alternar_contrasena)

        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.setObjectName("btnLogin")
        self.login_button.clicked.connect(self.iniciar_main_view)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Registrarse")
        self.register_button.clicked.connect(self.iniciar_register)
        layout.addWidget(self.register_button)
        self.show()

    def alternar_contrasena(self):
        self.password_visible = not self.password_visible
        mode = QLineEdit.EchoMode.Normal if self.password_visible else QLineEdit.EchoMode.Password
        self.password_input.setEchoMode(mode)
        icon = self.icono_ojo_abierto if self.password_visible else self.icono_ojo_cerrado
        self.action_ver_password.setIcon(icon)

    def iniciar_main_view(self):
        user_name = self.user_input.text().strip()
        password = self.password_input.text()
        if not user_name or not password:
            self.label_error.setText("Ingrese usuario y contraseña")
            return

        try:
            user = self.db_service.get_user_by_name(user_name)
            if user is None or user.get_password() != password:
                self.label_error.setText("Credencial incorrecta")
                return
            self.session_manager.set_current_user(user)
            self.open_main_window()
            self.close()
        except sqlite3.Error:
            self.label_error.setText("No se pudo acceder a la base de datos")
        except Exception as error:
            self.label_error.setText(f"Error en servidor: {error}")

    def iniciar_register(self):
        self.new_user_form = Register(self)
        self.new_user_form.show()
        self.hide()

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    sys.exit(app.exec())
