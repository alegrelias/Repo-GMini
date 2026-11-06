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
        self.setFixedSize(600, 500)
        self.setWindowTitle("Registro - GMini")
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
            QPushButton#btnPrincipal {
                background-color: #2f5275; font-weight: bold;
            }
        """)
        layout = QVBoxLayout(self)
        title = QLabel("GMini                                      LEAB")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #D8DEE9;")
        layout.addWidget(title)

        heading = QLabel("Crear cuenta")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(heading)
        self.label_error = QLabel("")
        self.label_error.setStyleSheet("color: #ff5555; font-size: 14px;")
        self.label_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_error)

        self.user_input = self._add_field(layout, "Usuario")
        self.email_input = self._add_field(layout, "Email")
        self.password_input_1 = self._add_password_field(layout, "Contraseña", 1)
        self.password_input_2 = self._add_password_field(layout, "Reingrese la Contraseña", 2)

        self.register_button = QPushButton("Registrarse")
        self.register_button.setObjectName("btnPrincipal")
        self.register_button.clicked.connect(self.iniciar_main_view)
        layout.addWidget(self.register_button)
        self.cancel_button = QPushButton("Volver al Inicio Sesion")
        self.cancel_button.clicked.connect(self.cerrar_registro)
        layout.addWidget(self.cancel_button)
        self.show()

    def _add_field(self, layout, label):
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        field = QLineEdit()
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_registro = Register()
    sys.exit(app.exec())
