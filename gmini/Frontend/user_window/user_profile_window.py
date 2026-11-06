import sys
import re
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtGui import QPixmap
from gmini.Backend.app.db.databaseService import DataBaseService
from gmini.Backend.app.services.sessionManager import SessionManager


class UserProfileWindow(QMainWindow):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.session_manager = SessionManager()
        self.db_service = getattr(main_window, "db_service", None) or DataBaseService()
        self.setObjectName("UserProfileWindow")
        self.setStyleSheet("background-color: #1e1e2e; color: #cdd6f4;")
        self.inicializar_ui()
        self._load_current_user()

    def inicializar_ui(self):
        self.setWindowTitle("GMini")
        self.setFixedSize(1280, 720)

        topWidget = QWidget()
        topLayout = QHBoxLayout()
        
        topWidget.setMaximumHeight(50)
        topWidget.setLayout(topLayout)

        bottomWidget = QWidget()
        bottomWidget.setStyleSheet("QFrame { background-color: #313244; border: 1px solid #313244; border-radius: 5px; }")
        bottomLayout = QHBoxLayout()
        bottomWidget.setLayout(bottomLayout)

        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(topWidget)
        central_layout.addWidget(bottomWidget)
        self.setCentralWidget(central_widget)

        titleLabel = QLabel("GMini")
        ownerLabel = QLabel("LEAB")

        self.btn_volver = QPushButton("< Volver")
        self.btn_volver.setStyleSheet("background-color: transparent; font-weight: bold; border: 1px solid #5a6b7d; border-radius: 5px; padding: 5px 15px;")
        self.btn_volver.clicked.connect(self.volver_main)

        topLayout.addWidget(self.btn_volver)
        topLayout.addWidget(titleLabel)
        topLayout.addStretch()
        topLayout.addWidget(ownerLabel)

        topLayout.addWidget(titleLabel)
        topLayout.addStretch()
        topLayout.addWidget(ownerLabel)

        # Frame de usuario
        userFrame = QFrame()
        frameLayout = QVBoxLayout()

        userFrame.setFrameShape(QFrame.Shape.StyledPanel)
        userFrame.setLayout(frameLayout)

        imageLabel = QLabel()
        imageLabel.setPixmap(QPixmap("gmini/Resources/default_avatar.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        imageLabel.setMaximumSize(100, 100)

        self.username_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.username_label.setMaximumHeight(30)
        self.username_label.setStyleSheet("font-size: 16px;")

        self.email_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.email_label.setMaximumHeight(30)

        logoutButton = QPushButton("Cerrar sesion")
        logoutButton.setMaximumHeight(30)
        logoutButton.clicked.connect(self.logout)

        frameLayout.addWidget(imageLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        frameLayout.addWidget(self.username_label)
        frameLayout.addWidget(self.email_label)
        frameLayout.addWidget(logoutButton)
        frameLayout.addStretch()

        bottomLayout.addWidget(userFrame)

        # Frame de cambio de nombre
        changeUsernameFrame = QFrame()
        changeUsernameLayout = QVBoxLayout()

        changeUsernameFrame.setFrameShape(QFrame.Shape.StyledPanel)
        changeUsernameFrame.setLayout(changeUsernameLayout)

        changeUsernameLabel = QLabel("Cambiar nombre", alignment=Qt.AlignmentFlag.AlignCenter)
        changeUsernameLabel.setMaximumHeight(30)

        self.new_username_field = QLineEdit()
        self.new_username_field.setPlaceholderText("Nuevo nombre")
        self.new_username_field.setMaximumHeight(30)

        self.username_password_field = QLineEdit()
        self.username_password_field.setPlaceholderText("Contraseña")
        self.username_password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.username_password_field.setMaximumHeight(30)

        confirmUsernameButton = QPushButton("Cambiar nombre")
        confirmUsernameButton.setMaximumHeight(30)
        confirmUsernameButton.clicked.connect(self.change_username)

        changeUsernameLayout.addWidget(changeUsernameLabel)
        changeUsernameLayout.addWidget(self.new_username_field)
        changeUsernameLayout.addWidget(self.username_password_field)
        changeUsernameLayout.addWidget(confirmUsernameButton)
        changeUsernameLayout.addStretch()

        bottomLayout.addWidget(changeUsernameFrame)

        # Frame de cambio de mail

        changeEmailFrame = QFrame()
        changeEmailLayout = QVBoxLayout()

        changeEmailFrame.setFrameShape(QFrame.Shape.StyledPanel)
        changeEmailFrame.setLayout(changeEmailLayout)

        changeEmailLabel = QLabel("Cambiar correo", alignment=Qt.AlignmentFlag.AlignCenter)
        changeEmailLabel.setMaximumHeight(30)

        self.old_email_field = QLineEdit()
        self.old_email_field.setPlaceholderText("Correo actual")
        self.old_email_field.setMaximumHeight(30)

        self.new_email_field = QLineEdit()
        self.new_email_field.setPlaceholderText("Nuevo correo")
        self.new_email_field.setMaximumHeight(30)

        self.email_password_field = QLineEdit()
        self.email_password_field.setPlaceholderText("Contraseña")
        self.email_password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.email_password_field.setMaximumHeight(30)

        confirmEmailButton = QPushButton("Cambiar correo")
        confirmEmailButton.setMaximumHeight(30)
        confirmEmailButton.clicked.connect(self.change_email)

        changeEmailLayout.addWidget(changeEmailLabel)
        changeEmailLayout.addWidget(self.old_email_field)
        changeEmailLayout.addWidget(self.new_email_field)
        changeEmailLayout.addWidget(self.email_password_field)
        changeEmailLayout.addWidget(confirmEmailButton)
        changeEmailLayout.addStretch()

        bottomLayout.addWidget(changeEmailFrame)

        # Frame de cambio de contraseña

        changePasswordFrame = QFrame()
        changePasswordLayout = QVBoxLayout()

        changePasswordFrame.setFrameShape(QFrame.Shape.StyledPanel)
        changePasswordFrame.setLayout(changePasswordLayout)

        changePasswordLabel = QLabel("Cambiar contraseña", alignment=Qt.AlignmentFlag.AlignCenter)
        changePasswordLabel.setMaximumHeight(30)

        self.old_password_field = QLineEdit()
        self.old_password_field.setPlaceholderText("Contraseña actual")
        self.old_password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.old_password_field.setMaximumHeight(30)

        self.new_password_field = QLineEdit()
        self.new_password_field.setPlaceholderText("Nueva contraseña")
        self.new_password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password_field.setMaximumHeight(30)

        self.confirm_password_field = QLineEdit()
        self.confirm_password_field.setPlaceholderText("Confirmar nueva contraseña")
        self.confirm_password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_field.setMaximumHeight(30)

        confirmPasswordButton = QPushButton("Cambiar contraseña")
        confirmPasswordButton.setMaximumHeight(30)
        confirmPasswordButton.clicked.connect(self.change_password)

        changePasswordLayout.addWidget(changePasswordLabel)
        changePasswordLayout.addWidget(self.old_password_field)
        changePasswordLayout.addWidget(self.new_password_field)
        changePasswordLayout.addWidget(self.confirm_password_field)
        changePasswordLayout.addWidget(confirmPasswordButton)
        changePasswordLayout.addStretch()

        bottomLayout.addWidget(changePasswordFrame)

        central_layout.addStretch()



    def volver_main(self):
        if self.main_window:
            self.main_window.show() # Muestra la ventana principal
        self.close()                # Cierra la ventana de perfil


    def logout(self):
        self.session_manager.clear_session()
        if self.main_window:
            self.main_window.close()
        self.close()

    def _load_current_user(self):
        user = self.session_manager.get_current_user()
        if user is None:
            self.username_label.setText("Sin sesión")
            self.email_label.setText("")
            return
        self.username_label.setText(user.get_user_name())
        self.email_label.setText(user.get_email())

    def _show_error(self, title, message):
        QMessageBox.warning(self, title, message)

    def _show_success(self, message):
        QMessageBox.information(self, "Perfil actualizado", message)

    def _current_user_and_password(self, password):
        user = self.session_manager.get_current_user()
        if user is None:
            self._show_error("Sesión", "No hay un usuario iniciado sesión.")
            return None
        if not password or password != user.get_password():
            self._show_error("Autenticación", "La contraseña actual es incorrecta.")
            return None
        return user

    def _persist(self, user, method_name, value):
        user_id = user.get_id()
        if user_id is None:
            return True
        return getattr(self.db_service, method_name)(user_id, value)

    def change_username(self, checked=False):
        new_name = self.new_username_field.text().strip()
        user = self._current_user_and_password(self.username_password_field.text())
        if user is None:
            return
        if not new_name:
            self._show_error("Nombre", "Ingrese un nombre nuevo.")
            return
        if new_name == user.get_user_name():
            self._show_error("Nombre", "El nombre nuevo debe ser diferente.")
            return
        try:
            if not self._persist(user, "update_user_name", new_name):
                raise ValueError("No se pudo actualizar el nombre en la base de datos.")
        except Exception as error:
            self._show_error("Nombre", f"No se pudo cambiar el nombre: {error}")
            return
        user.set_user_name(new_name)
        self.username_label.setText(new_name)
        self.new_username_field.clear()
        self.username_password_field.clear()
        self._show_success("El nombre se cambió correctamente.")

    def change_email(self, checked=False):
        old_email = self.old_email_field.text().strip()
        new_email = self.new_email_field.text().strip()
        user = self._current_user_and_password(self.email_password_field.text())
        if user is None:
            return
        if old_email != user.get_email():
            self._show_error("Correo", "El correo actual no coincide.")
            return
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", new_email):
            self._show_error("Correo", "Ingrese un correo válido.")
            return
        if new_email == old_email:
            self._show_error("Correo", "El correo nuevo debe ser diferente.")
            return
        try:
            if not self._persist(user, "update_user_email", new_email):
                raise ValueError("No se pudo actualizar el correo en la base de datos.")
        except Exception as error:
            self._show_error("Correo", f"No se pudo cambiar el correo: {error}")
            return
        user.set_email(new_email)
        self.email_label.setText(new_email)
        self.old_email_field.clear()
        self.new_email_field.clear()
        self.email_password_field.clear()
        self._show_success("El correo se cambió correctamente.")

    def change_password(self, checked=False):
        old_password = self.old_password_field.text()
        new_password = self.new_password_field.text()
        confirmation = self.confirm_password_field.text()
        user = self._current_user_and_password(old_password)
        if user is None:
            return
        if not new_password:
            self._show_error("Contraseña", "Ingrese una contraseña nueva.")
            return
        if new_password != confirmation:
            self._show_error("Contraseña", "Las contraseñas nuevas no coinciden.")
            return
        if new_password == old_password:
            self._show_error("Contraseña", "La contraseña nueva debe ser diferente.")
            return
        try:
            if not self._persist(user, "update_user_password", new_password):
                raise ValueError("No se pudo actualizar la contraseña en la base de datos.")
        except Exception as error:
            self._show_error("Contraseña", f"No se pudo cambiar la contraseña: {error}")
            return
        user.set_password(new_password)
        self.old_password_field.clear()
        self.new_password_field.clear()
        self.confirm_password_field.clear()
        self._show_success("La contraseña se cambió correctamente.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserProfileWindow()
    window.show()
    sys.exit(app.exec())