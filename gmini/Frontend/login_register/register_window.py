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
from gmini.Backend.app.models.user import User


class Register(QWidget):
    def __init__(self, ventana_login=None):
        super().__init__()
        self.ventana_login = ventana_login
        self.db_service = getattr(ventana_login, "db_service", None) or DataBaseService()
        self.password_visible_1 = False
        self.password_visible_2 = False
        self.inicializar_ui()

    def inicializar_ui(self):
        self.setFixedSize(560, 520)
        self.setWindowTitle("Registro - GMini")
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
                min-width: 250px;
                max-width: 250px;
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
            QPushButton#btnPrincipal {
                background-color: #2f5275; 
                font-weight: bold;
            }
            QPushButton#btnPrincipal:hover {
                background-color: #3b648f;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 25, 35, 25)
        layout.setSpacing(12)

        # Fila superior con Título GMini y LEAB perfectamente alineados
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

        heading = QLabel("Crear cuenta")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setStyleSheet("font-size: 20px; font-weight: bold; color: #E5E9F0; margin-bottom: 5px;")
        layout.addWidget(heading)
        
        self.label_error = QLabel("")
        self.label_error.setStyleSheet("color: #ff5555; font-size: 13px;")
        self.label_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_error)

        self.user_input = self._add_field(layout, "Usuario")
        self.email_input = self._add_field(layout, "Email")
        self.password_input_1 = self._add_password_field(layout, "Contraseña", 1)
        self.password_input_2 = self._add_password_field(layout, "Reingrese la Contraseña", 2)

        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(10)
        
        self.register_button = QPushButton("Registrarse")
        self.register_button.setObjectName("btnPrincipal")
        self.register_button.clicked.connect(self.iniciar_main_view)
        btn_layout.addWidget(self.register_button)
        
        self.cancel_button = QPushButton("Volver al Inicio Sesion")
        self.cancel_button.clicked.connect(self.cerrar_registro)
        btn_layout.addWidget(self.cancel_button)
        
        layout.addLayout(btn_layout)

        # Navegación por Enter
        self.user_input.returnPressed.connect(self.email_input.setFocus)
        self.email_input.returnPressed.connect(self.password_input_1.setFocus)
        self.password_input_1.returnPressed.connect(self.password_input_2.setFocus)
        self.password_input_2.returnPressed.connect(self.iniciar_main_view)

        self.show()

    def _add_field(self, layout, label):
        row = QHBoxLayout()
        lbl = QLabel(label)
        lbl.setFixedSize(180, 30) # Ancho fijo para las etiquetas de texto de la izquierda para perfecta simetría
        field = QLineEdit()
        row.addWidget(lbl)
        row.addWidget(field)
        layout.addLayout(row)
        return field

    def _add_password_field(self, layout, label, number):
        field = self._add_field(layout, label)
        field.setEchoMode(QLineEdit.EchoMode.Password)
        resources = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Resources"))
        closed = QIcon(os.path.join(resources, "ojo_cerrado.jpg"))
        opened = QIcon(os.path.join(resources, "ojo_abierto.jpg"))
        action = field.addAction(closed, QLineEdit.ActionPosition.TrailingPosition)
        action.triggered.connect(lambda: self.alternar_contrasena(number, field, action, closed, opened))
        return field

    def alternar_contrasena(self, number, field, action, closed, opened):
        visible = not getattr(self, f"password_visible_{number}")
        setattr(self, f"password_visible_{number}", visible)
        field.setEchoMode(QLineEdit.EchoMode.Normal if visible else QLineEdit.EchoMode.Password)
        action.setIcon(opened if visible else closed)

    def iniciar_main_view(self):
        usuario = self.user_input.text().strip()
        email = self.email_input.text().strip()
        password1 = self.password_input_1.text()
        password2 = self.password_input_2.text()
        if not usuario or not email or not password1 or not password2:
            self.label_error.setText("Ingrese usuario, email y contraseña")
        elif password1 != password2:
            self.label_error.setText("Las contraseñas no coinciden")
        else:
            try:
                if self.db_service.get_user_by_name(usuario) is not None:
                    self.label_error.setText("El usuario ya existe")
                    return
                if self.db_service.get_user_by_email(email) is not None:
                    self.label_error.setText("El email ya está registrado")
                    return
                self.db_service.save_user(User(usuario, email, password1))
                self.cerrar_registro()
            except sqlite3.IntegrityError:
                self.label_error.setText("El usuario o email ya está registrado")
            except sqlite3.Error:
                self.label_error.setText("No se pudo acceder a la base de datos")
            except Exception as error:
                self.label_error.setText(f"Error en servidor: {error}")

    def cerrar_registro(self):
        if self.ventana_login:
            self.ventana_login.show()
        self.close()