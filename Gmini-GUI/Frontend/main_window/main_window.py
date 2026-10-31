import sys
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QMenu,
    QGridLayout,
    QSizePolicy,
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt

class Mainwindow(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializar_ui()

    def inicializar_ui(self):
        self.setFixedSize(1280, 720)
        self.setWindowTitle("Pantalla Principal")

        layout = QVBoxLayout()
        toolbar = QToolBar()
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)

        opciones = (
            ("Nueva sesion", self.nueva_sesion),
            ("Graficas", self.graficas),
            ("Calibracion", self.calibracion),
            ("Analisis", self.analisis),
            ("Exportar", self.exportar),
            ("Importar", self.importar),
            ("Guardar", self.guardar),
        )
        for nombre, funcion in opciones:
            toolbar.addAction(nombre, funcion)

        menu_ver = QMenu("Ver", self)
        boton_ver = QToolButton()
        boton_ver.setText("Ver")
        boton_ver.setMenu(menu_ver)
        boton_ver.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        toolbar.addWidget(boton_ver)

        layout.addWidget(toolbar)
        mensaje = QLabel("¡Bienvenido a la Pantalla Principal!")
        mensaje.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(mensaje)

        widgets_layout = QGridLayout()
        for indice, placeholder in enumerate(
            ("Placeholder 1", "Placeholder 2", "Placeholder 3", "Placeholder 4")
        ):
            widget = CollapsibleWidget(placeholder)
            widgets_layout.addWidget(widget, indice // 2, indice % 2)

        layout.addLayout(widgets_layout)
        self.setLayout(layout)

    def nueva_sesion(self):
        pass

    def graficas(self):
        pass

    def calibracion(self):
        pass

    def analisis(self):
        pass

    def exportar(self):
        pass

    def importar(self):
        pass

    def guardar(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_login = Mainwindow()
    ventana_login.show()
    sys.exit(app.exec())