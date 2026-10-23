import sys 
import os
from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem,QSizePolicy, QMessageBox)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

class Register(QWidget):
    def __init__(self, ventana_login=None):
        super().__init__()
        self.ventana_login = ventana_login 
        self.inicializar_ui()

    def inicializar_ui(self):
        self.setFixedSize(600,500)
        self.setWindowTitle("Registro - GMini")

        self.setStyleSheet("""
            QWidget {
                background-color: #2b2e33; 
                color: white;
            }
            QLabel {
                font-size: 16px;
            }
            QLineEdit {
                background-color: #2b2e33;
                border: 1px solid #5a6b7d;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton#btnPrincipal {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3a6085, stop:1 #223850);
                border: 1px solid #1c2e42;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton#btnPrincipal:hover {
                background-color: #4a7aa8;
            }
            QPushButton#btnSecundario {
                background-color: transparent;
                border: 1px solid #5a6b7d;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton#btnSecundario:hover {
                background-color: #383c42;
            }
        """)

        self.generar_formulario()
        self.show()

    def generar_formulario(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40,20,40,40)
        main_layout.setSpacing(20)

        titulo_label = QLabel("Crear cuenta")
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo_label.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        main_layout.addWidget(titulo_label)

        user_layout = QHBoxLayout()
        user_label = QLabel("Usuario")
        user_label.setFixedWidth(170)
        self.user_input = QLineEdit()
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.user_input)
        main_layout.addLayout(user_layout)

        email_layout = QHBoxLayout()
        email_label = QLabel("Email")
        email_label.setFixedWidth(170)
        self.email_input = QLineEdit()
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        main_layout.addLayout(email_layout)

        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_imagenes = os.path.abspath(os.path.join(ruta_script, "..", "..", "Resources"))

        password_layout_1 = QHBoxLayout()
        password_label_1 = QLabel("Contraseña")
        password_label_1.setFixedWidth(170)

        self.password_input_1 = QLineEdit()
        self.password_input_1.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.icono_ojo_cerrado1 = QIcon(os.path.join(ruta_imagenes, "ojo_cerrado.jpg"))
        self.icono_ojo_abierto1 = QIcon(os.path.join(ruta_imagenes, "ojo_abierto.jpg"))
        
        self.action_ver_password_1 = self.password_input_1.addAction(
            self.icono_ojo_cerrado1, QLineEdit.ActionPosition.TrailingPosition
        )
        self.action_ver_password_1.triggered.connect(self.alternar_contrasena_1)
        self.password_visible_1 = False

        password_layout_1.addWidget(password_label_1)
        password_layout_1.addWidget(self.password_input_1)
        main_layout.addLayout(password_layout_1)

        password_layout_2 = QHBoxLayout()
        password_label_2 = QLabel("Reingrese la Contraseña")
        password_label_2.setFixedWidth(170)
        
        self.password_input_2 = QLineEdit()
        self.password_input_2.setEchoMode(QLineEdit.EchoMode.Password)
                
        self.icono_ojo_cerrado2 = QIcon(os.path.join(ruta_imagenes, "ojo_cerrado.jpg"))
        self.icono_ojo_abierto2 = QIcon(os.path.join(ruta_imagenes, "ojo_abierto.jpg"))
                
        self.action_ver_password_2 = self.password_input_2.addAction(
            self.icono_ojo_cerrado2, QLineEdit.ActionPosition.TrailingPosition
        )
        self.action_ver_password_2.triggered.connect(self.alternar_contrasena_2)
        self.password_visible_2 = False
        
        password_layout_2.addWidget(password_label_2)
        password_layout_2.addWidget(self.password_input_2)
        main_layout.addLayout(password_layout_2)

        main_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        self.register_button = QPushButton("Registrarse")
        self.register_button.setObjectName("btnPrincipal")
        main_layout.addWidget(self.register_button)
        self.register_button.clicked.connect(self.iniciar_main_view)

        self.cancel_button = QPushButton("Volver al Inicio Sesion")
        self.cancel_button.setObjectName("btnSecundario")
        main_layout.addWidget(self.cancel_button)
        self.cancel_button.clicked.connect(self.cerrar_registro)

        self.setLayout(main_layout)

    def alternar_contrasena_1(self):
        self.password_visible_1 = not self.password_visible_1
        if self.password_visible_1:
            self.password_input_1.setEchoMode(QLineEdit.EchoMode.Normal)
            self.action_ver_password_1.setIcon(self.icono_ojo_abierto1)
        else:
            self.password_input_1.setEchoMode(QLineEdit.EchoMode.Password)
            self.action_ver_password_1.setIcon(self.icono_ojo_cerrado1)

    def alternar_contrasena_2(self):
        self.password_visible_2 = not self.password_visible_2
        if self.password_visible_2:
            self.password_input_2.setEchoMode(QLineEdit.EchoMode.Normal)
            self.action_ver_password_2.setIcon(self.icono_ojo_abierto2)
        else:
            self.password_input_2.setEchoMode(QLineEdit.EchoMode.Password)
            self.action_ver_password_2.setIcon(self.icono_ojo_cerrado2)

    # A modificar a futuro
    def iniciar_main_view(self):
        user_path = 'usuario.txt'
        usuario = self.user_input.text()
        password1 = self.password_input_1.text()
        password2 = self.password_input_2.text()

        if password1 == '' or password2 == '' or usuario == '':
            QMessageBox.warning(self, 'Error',
            'Ingrese datos validos',
            QMessageBox.StandardButton.Close,
            QMessageBox.StandardButton.Close) 
        elif password1 != password2:
            QMessageBox.warning(self, 'Error',
            'Las contraseñas no coinciden',
            QMessageBox.StandardButton.Close,
            QMessageBox.StandardButton.Close) 
        else:
            try:
                with open(user_path, 'a+') as f:
                    f.write(f"{usuario},{password1}\n")
                QMessageBox.information(self, 'Creacion exitosa',
                'USuario creado correctamente',
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok)
                self.open_main_window() 
                self.hide()

            except FileNotFoundError as e:
                QMessageBox.warning(self, 'Error',
                f'La base de datos no existe:{e}',
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close)
    
    def cerrar_registro(self):
        if self.ventana_login:
            self.ventana_login.show()
        self.close()

    def open_main_window(self):
        import sys
        import os
        
        ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        if ruta_raiz not in sys.path:
            sys.path.append(ruta_raiz)
            
        from main_window.main_window import Mainwindow
        
        self.main_window_instance = Mainwindow()
        self.main_window_instance.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana_registro = Register()
    sys.exit(app.exec())