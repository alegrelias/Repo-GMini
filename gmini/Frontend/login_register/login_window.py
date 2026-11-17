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
        self.setFixedSize(500, 420)
        self.setWindowTitle("GMini GUI - Iniciar Sesión")
        
        # Fondo unificado exacto con el tono del Main (#1e2229) y campos de texto alineados
        self.setStyleSheet("""
            QWidget { 
                background-color: #1e2229; 
                color: white; 
                font-family: Arial, sans-serif;
            }
            QLabel { 
                font-size: 15px; 
            }
            QLineEdit {
                background-color: #282c34; 
                border: 1px solid #4f5b66;
                border-radius: 8px; 
                padding: 8px; 
                font-size: 14px;
                min-width: 240px;
                max-width: 240px;
            }
            QLineEdit:focus {
                border: 1px solid #61afef;
            }
            QPushButton {
                background-color: #3b4252;
                border: 1px solid #4f5b66; 
                border-radius: 8px;
                padding: 10px; 
                font-size: 15px;
                color: white;
            }
            QPushButton:hover {
                background-color: #434c5e;
            }
            QPushButton#btnLogin {
                background-color: #2f5275; 
                font-weight: bold;
            }
            QPushButton#btnLogin:hover {
                background-color: #3b648f;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 25, 35, 25)
        layout.setSpacing(15)

        # Fila superior con Título GMini y etiqueta LEAB alineada a la derecha
        top_layout = QHBoxLayout()
        title = QLabel("GMini")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #D8DEE9;")
        
        label_leab = QLabel("LEAB")
        label_leab.setStyleSheet("font-size: 20px; font-weight: bold; color: #D8DEE9;")
        label_leab.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(label_leab)
        layout.addLayout(top_layout)

        self.label_error = QLabel("")
        self.label_error.setStyleSheet("color: #ff5555; font-size: 13px;")
        self.label_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_error)

        # Campos distribuidos uniformemente para perfecta alineación visual
        user_layout = QHBoxLayout()
        lbl_user = QLabel("Usuario")
        lbl_user.setFixedSize(90, 30)
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Ingrese usuario")
        user_layout.addWidget(lbl_user)
        user_layout.addWidget(self.user_input)
        layout.addLayout(user_layout)

        password_layout = QHBoxLayout()
        lbl_pass = QLabel("Contraseña")
        lbl_pass.setFixedSize(90, 30)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Ingrese contraseña")
        password_layout.addWidget(lbl_pass)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        resources = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Resources"))
        self.icono_ojo_cerrado = QIcon(os.path.join(resources, "ojo_cerrado.jpg"))
        self.icono_ojo_abierto = QIcon(os.path.join(resources, "ojo_abierto.jpg"))
        self.action_ver_password = self.password_input.addAction(
            self.icono_ojo_cerrado, QLineEdit.ActionPosition.TrailingPosition
        )
        self.action_ver_password.triggered.connect(self.alternar_contrasena)

        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(10)
        
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.setObjectName("btnLogin")
        self.login_button.clicked.connect(self.iniciar_main_view)
        btn_layout.addWidget(self.login_button)

        self.register_button = QPushButton("Registrarse")
        self.register_button.clicked.connect(self.iniciar_register)
        btn_layout.addWidget(self.register_button)
        
        layout.addLayout(btn_layout)

        # Tecla Enter
        self.user_input.returnPressed.connect(self.password_input.setFocus)
        self.password_input.returnPressed.connect(self.iniciar_main_view)

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