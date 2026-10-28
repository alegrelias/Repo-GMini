import os
import sys  
from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy) 
from PyQt6.QtGui import QFont, QPixmap, QIcon 
from PyQt6.QtCore import Qt 
from register_window import Register 

class Login(QWidget):     
    def __init__(self):         
        super().__init__()         
        self.inializacion_ui()     

    def inializacion_ui(self):         
        self.setFixedSize(400, 520)
        self.setWindowTitle("GMini GUI")         
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
                font-size: 16px;             }             
            QPushButton#btnRegister:hover {                 
                background-color: #383c42;             }         
        """)              
        self.generar_formulario()         
        self.show()              

    def generar_formulario(self):         
        main_layout = QVBoxLayout()         
        main_layout.setContentsMargins(40, 20, 40, 40)         
        main_layout.setSpacing(15)         

        top_layout = QHBoxLayout()
        title_label = QLabel("GMini")
        title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #D8DEE9;")
        owner_label = QLabel("LEAB")
        owner_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #D8DEE9;")
        
        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addWidget(owner_label)
        main_layout.addLayout(top_layout)

        main_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))         

        #Etiqueta para mostrar errores en la interfaz en color rojo
        self.label_error = QLabel("")
        self.label_error.setStyleSheet("color: #ff5555; font-size: 14px;")
        self.label_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.label_error)

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
        
        self.password_input = QLineEdit()         
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)         
        ruta_script = os.path.dirname(os.path.abspath(__file__))         
        ruta_imagenes = os.path.abspath(os.path.join(ruta_script, "..", "..", "Resources"))         
        
        ruta_cerrado = os.path.join(ruta_imagenes, "ojo_cerrado.jpg")         
        ruta_abierto = os.path.join(ruta_imagenes, "ojo_abierto.jpg")                  
        
        self.icono_ojo_cerrado = QIcon(ruta_cerrado)         
        self.icono_ojo_abierto = QIcon(ruta_abierto)                  
        
        self.action_ver_password = self.password_input.addAction(             
            self.icono_ojo_cerrado,              
            QLineEdit.ActionPosition.TrailingPosition         
        )         
        self.action_ver_password.triggered.connect(self.alternar_contrasena)                  
        self.password_visible = False         
        
        password_layout.addWidget(password_label)         
        password_layout.addWidget(self.password_input)         
        main_layout.addLayout(password_layout)         
        
        main_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))         
        
        self.login_button = QPushButton("Iniciar Sesión")         
        self.login_button.setObjectName("btnLogin")         
        main_layout.addWidget(self.login_button)         
        self.login_button.clicked.connect(self.iniciar_main_view)         

        self.register_button = QPushButton("Registrarse")         
        self.register_button.setObjectName("btnRegister")         
        main_layout.addWidget(self.register_button)         
        self.register_button.clicked.connect(self.iniciar_register)         
        
        self.setLayout(main_layout)     

    def alternar_contrasena(self):         
        self.password_visible = not self.password_visible                  
        if self.password_visible:             
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)             
            self.action_ver_password.setIcon(self.icono_ojo_abierto)         
        else:             
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
                self.is_logget = True                 
                self.open_main_window()                 
                self.close()                              
            else:                 
                self.label_error.setText("Credencial incorrecta") 
        except FileNotFoundError as e:             
            self.label_error.setText(f"Base de datos no encontrada") 
        except Exception as e:                     
            self.label_error.setText(f"Error en servidor: {e}") 

    def iniciar_register(self):         
        self.new_user_form = Register(self)         
        self.new_user_form.show()         
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