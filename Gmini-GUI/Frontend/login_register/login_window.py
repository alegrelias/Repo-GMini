import os
import sys 
from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt
from register_window import Register



class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.inializacion_ui()

    def inializacion_ui(self):
        self.setFixedSize(400, 500)
        self.setWindowTitle("GMini GUI")
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2e33; /* Fondo gris oscuro */
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
            QPushButton#btnLogin {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3a6085, stop:1 #223850);
                border: 1px solid #1c2e42;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton#btnLogin:hover {
                background-color: #4a7aa8;
            }
            QPushButton#btnRegister {
                background-color: transparent;
                border: 1px solid #5a6b7d;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton#btnRegister:hover {
                background-color: #383c42;
            }
        """)
    
        self.generar_formulario()
        self.show()
        

    def generar_formulario(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 20, 40, 40)
        main_layout.setSpacing(20)


        self.img_label = QLabel(self)
        self.img_label.setText("[ ICONO ]")
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.img_label)

        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        
        user_layout = QHBoxLayout()
        user_label = QLabel("Usuario")
        user_label.setFixedWidth(80)
        self.user_input = QLineEdit()
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.user_input)
        main_layout.addLayout(user_layout)

        password_layout = QHBoxLayout()
        password_label = QLabel("Contraseña")
        password_label.setFixedWidth(80)

        #Configuracion de los ojos
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_imagenes = os.path.abspath(os.path.join(ruta_script, "..", "..", "Resources"))

        # iconos de ojos abiertos y cerrados usando la ruta exacta
        ruta_cerrado = os.path.join(ruta_imagenes, "ojo_cerrado.jpg")
        ruta_abierto = os.path.join(ruta_imagenes, "ojo_abierto.jpg")

        print("Buscando el ojo cerrado en:", ruta_cerrado)
        
        # Cargar los íconos
        self.icono_ojo_cerrado = QIcon(ruta_cerrado)
        self.icono_ojo_abierto = QIcon(ruta_abierto)
        
        # Agregamos la acción (el ícono) a la derecha de la caja de texto
        self.action_ver_password = self.password_input.addAction(
            self.icono_ojo_cerrado, 
            QLineEdit.ActionPosition.TrailingPosition
        )
        
        # Conectamos el clic en el ícono con la función
        self.action_ver_password.triggered.connect(self.alternar_contrasena)
        
        self.password_visible = False

        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        main_layout.addLayout(password_layout)

        main_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # boton de login
        self.login_button = QPushButton("Iniciar Sesion")
        self.login_button.setObjectName("btnLogin")
        main_layout.addWidget(self.login_button)
        self.login_button.clicked.connect(self.iniciar_main_view)

        # boton de registro
        self.register_button = QPushButton("Registrarse")
        self.register_button.setObjectName("btnRegister")
        main_layout.addWidget(self.register_button)
        self.register_button.clicked.connect(self.iniciar_register)

        self.setLayout(main_layout)

    def alternar_contrasena(self):
        self.password_visible = not self.password_visible
        
        if self.password_visible:
            # abre el ojo Y muestra la contraseña 
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.action_ver_password.setIcon(self.icono_ojo_abierto)
        else:
            # Cierra el ojo y no muestra la contraseña
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.action_ver_password.setIcon(self.icono_ojo_cerrado)

    # A modificar a futuro
    def iniciar_main_view(self):
        users = []
        user_path = 'usuario.txt'

        try: 

            with open(user_path, 'r') as f:
                for linea in f:
                    users.append(linea.strip("\n"))
            login_informacion = f"{self.user_input.text()},{self.password_input.text()}"

            if login_informacion in users:
                QMessageBox.information(self, "inicio de sesion",
                "Inicio de sesion exitoso",
                QMessageBox.StandardButton.Ok)
                self.is_logget = True
                self.open_main_window()
                self.close()
                
            else:
                QMessageBox.warning(self, "Error",
                "Credencial incorrecta",
                QMessageBox.StandardButton.Close)

        except FileNotFoundError as e:
            QMessageBox.warning(self, "Error",
            f"Base de datos de usuario no encontrada: {e}",
            QMessageBox.StandardButton.Close)

        except Exception as e:
                    QMessageBox.warning(self, "Error",
                    f"Error en servidor: {e}",
                    QMessageBox.StandardButton.Close)

    def iniciar_register(self):
        self.new_user_from = Register(self)
        self.new_user_from.show()
        self.hide()

    def open_main_window(self):
        ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        if ruta_raiz not in sys.path:
            sys.path.append(ruta_raiz)
            
        from main_window.main_window import Mainwindow
        
        self.main_window = Mainwindow()
        self.main_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()
    sys.exit(app.exec())