import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtGui import QPixmap

class UserProfileWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GMini")
        self.setFixedSize(1280, 720)

        topWidget = QWidget()
        topLayout = QHBoxLayout()
        
        topWidget.setMaximumHeight(50)
        topWidget.setLayout(topLayout)

        bottomLayout = QHBoxLayout()

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(topWidget)
        self.layout().addLayout(bottomLayout)

        titleLabel = QLabel("GMini")
        ownerLabel = QLabel("LEAB")

        topLayout.addWidget(titleLabel)
        topLayout.addStretch()
        topLayout.addWidget(ownerLabel)

        # Frame de usuario
        userFrame = QFrame()
        frameLayout = QVBoxLayout()

        userFrame.setFrameShape(QFrame.Shape.StyledPanel)
        userFrame.setLayout(frameLayout)

        imageLabel = QLabel()
        imageLabel.setPixmap(QPixmap("Gmini-GUI/Resources/Default Avatar.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        imageLabel.setMaximumSize(100, 100)

        usernameLabel = QLabel("Username: JohnDoe", alignment=Qt.AlignmentFlag.AlignCenter)
        usernameLabel.setMaximumHeight(30)

        emailLabel = QLabel("Email: johndoe@example.com", alignment=Qt.AlignmentFlag.AlignCenter)
        emailLabel.setMaximumHeight(30)

        logoutButton = QPushButton("Cerrar sesion")
        logoutButton.setMaximumHeight(30)
        logoutButton.clicked.connect(self.logout)

        frameLayout.addWidget(imageLabel)
        frameLayout.addWidget(usernameLabel)
        frameLayout.addWidget(emailLabel)
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

        newUsernameField = QLineEdit()
        newUsernameField.setPlaceholderText("Nuevo nombre")
        newUsernameField.setMaximumHeight(30)

        usernamePasswordField = QLineEdit()
        usernamePasswordField.setPlaceholderText("Contraseña")
        usernamePasswordField.setEchoMode(QLineEdit.EchoMode.Password)
        usernamePasswordField.setMaximumHeight(30)

        confirmUsernameButton = QPushButton("Cambiar nombre")
        confirmUsernameButton.setMaximumHeight(30)
        confirmUsernameButton.clicked.connect(self.change_username)

        changeUsernameLayout.addWidget(changeUsernameLabel)
        changeUsernameLayout.addWidget(newUsernameField)
        changeUsernameLayout.addWidget(usernamePasswordField)
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

        oldEmailField = QLineEdit()
        oldEmailField.setPlaceholderText("Correo actual")
        oldEmailField.setMaximumHeight(30)

        newEmailField = QLineEdit()
        newEmailField.setPlaceholderText("Nuevo correo")
        newEmailField.setMaximumHeight(30)

        emailPasswordField = QLineEdit()
        emailPasswordField.setPlaceholderText("Contraseña")
        emailPasswordField.setEchoMode(QLineEdit.EchoMode.Password)
        emailPasswordField.setMaximumHeight(30)

        confirmEmailButton = QPushButton("Cambiar correo")
        confirmEmailButton.setMaximumHeight(30)
        confirmEmailButton.clicked.connect(self.change_email)

        changeEmailLayout.addWidget(changeEmailLabel)
        changeEmailLayout.addWidget(oldEmailField)
        changeEmailLayout.addWidget(newEmailField)
        changeEmailLayout.addWidget(emailPasswordField)
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

        oldPasswordField = QLineEdit()
        oldPasswordField.setPlaceholderText("Contraseña actual")
        oldPasswordField.setEchoMode(QLineEdit.EchoMode.Password)
        oldPasswordField.setMaximumHeight(30)

        newPasswordField = QLineEdit()
        newPasswordField.setPlaceholderText("Nueva contraseña")
        newPasswordField.setEchoMode(QLineEdit.EchoMode.Password)
        newPasswordField.setMaximumHeight(30)

        confirmPasswordField = QLineEdit()
        confirmPasswordField.setPlaceholderText("Confirmar nueva contraseña")
        confirmPasswordField.setEchoMode(QLineEdit.EchoMode.Password)
        confirmPasswordField.setMaximumHeight(30)

        confirmPasswordButton = QPushButton("Cambiar contraseña")
        confirmPasswordButton.setMaximumHeight(30)
        confirmPasswordButton.clicked.connect(self.change_password)

        changePasswordLayout.addWidget(changePasswordLabel)
        changePasswordLayout.addWidget(oldPasswordField)
        changePasswordLayout.addWidget(newPasswordField)
        changePasswordLayout.addWidget(confirmPasswordField)
        changePasswordLayout.addWidget(confirmPasswordButton)
        changePasswordLayout.addStretch()

        bottomLayout.addWidget(changePasswordFrame)

        self.layout().addStretch()


    def logout(self):
        pass

    def change_username(self):
        pass

    def change_email(self):
        pass

    def change_password(self):
        pass


app = QApplication(sys.argv)
window = UserProfileWindow()
window.show()
app.exec()