import sys
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt


class Mainwindow(QWidget): 
    def __init__(self):
       
        super().__init__() 
        self.inicializar_ui()

    def inicializar_ui(self):
        self.setFixedSize(600, 400)
        self.setWindowTitle("Pantalla Principal")
        self.setStyleSheet("background-color: #2b2e33; color: white;")

        layout = QVBoxLayout()
        mensaje = QLabel("¡Bienvenido a la Pantalla Principal!")
        mensaje.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(mensaje)
        
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_login = Mainwindow()
    ventana_login.show()
    sys.exit(app.exec())