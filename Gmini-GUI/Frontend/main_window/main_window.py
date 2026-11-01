from ast import main
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QGridLayout,
    QPushButton,
    QSizePolicy,
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt

class CollapseFrame(QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
        self.is_collapsed = False

        self.toggle_button = QPushButton(text=self.title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)
        self.toggle_button.clicked.connect(self.toggle)

        self.setFrameShape(QFrame.Shape.Box)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.toggle_button)
        main_layout.addWidget(self.content_widget)
        self.setLayout(main_layout)


    def toggle(self):
        if self.is_collapsed:
            self.content_widget.show()
            self.is_collapsed = False
        else:
            self.content_widget.hide()
            self.is_collapsed = True

    def add_widget(self, widget):
        self.content_layout.addWidget(widget)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializar_ui()

    def inicializar_ui(self):
        self.setFixedSize(1280, 720)
        self.setWindowTitle("Pantalla Principal")

        layout = QVBoxLayout()
        mainWidget = QWidget()
        toolbar = QToolBar()

        toolbar.addAction("Nueva sesion", self.nueva_sesion)
        toolbar.addAction("Graficas", self.graficas)
        toolbar.addAction("Calibracion", self.calibracion)
        toolbar.addAction("Analisis", self.analisis)
        toolbar.addAction("Exportar", self.exportar)
        toolbar.addAction("Importar", self.importar)
        toolbar.addAction("Guardar", self.guardar)

        layout.addWidget(toolbar)
        layout.addWidget(mainWidget)
        mainWidget.setLayout(QHBoxLayout())

        leftFrame = QFrame()
        leftFrame.setFrameShape(QFrame.Shape.Box)
        leftLayout = QVBoxLayout()
        leftFrame.setLayout(leftLayout)

        middleFrame = QFrame()
        middleFrame.setFrameShape(QFrame.Shape.Box)
        middleLayout = QVBoxLayout()
        middleFrame.setLayout(middleLayout)

        rightFrame = QFrame()
        rightFrame.setFrameShape(QFrame.Shape.Box)
        rightLayout = QVBoxLayout()
        rightFrame.setLayout(rightLayout)

        mensaje = QLabel("¡Bienvenido a la Pantalla Principal!")
        mensaje.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        mainWidget.layout().addWidget(leftFrame,1)
        mainWidget.layout().addWidget(middleFrame,3)
        mainWidget.layout().addWidget(rightFrame,1)

        conexionFrame = CollapseFrame("Conexion")
        conexionFrame.add_widget(QLabel("Contenido de Conexion"))
        leftLayout.addWidget(conexionFrame)


        leftLayout.addStretch()


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
    window = MainWindow()
    window.show()
    sys.exit(app.exec())