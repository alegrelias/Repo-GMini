from ast import main
import os,sys
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt, pyqtSignal

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

class TextBox(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.titleLabel = QLabel(self.title)
        self.layout.addWidget(self.titleLabel)

        self.valueBox = QLineEdit()
        self.valueBox.setStyleSheet("background-color: #45475a;")
        self.layout.addWidget(self.valueBox)

    def get_value(self):
        return self.valueBox.text()

    def set_value(self, value):
        self.valueBox.setText(value)

class CollapseWidget(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
        self.is_collapsed = False 
        self.setStyleSheet("background-color: #313244;")

        self.toggle_button = QPushButton(text=self.title)
        self.toggle_button.setStyleSheet("background-color: #313244;")
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)
        self.toggle_button.clicked.connect(self.toggle)

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

    def layout(self):
        return self.content_layout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e; color: #cdd6f4;
            }
        """)
        self.inicializar_ui()

    def inicializar_ui(self):
        self.setFixedSize(1280, 720)
        self.setWindowTitle("Pantalla Principal")

        layout = QVBoxLayout()
        titleWidget = QWidget()
        toolbar = QToolBar()
        mainWidget = QWidget()

        titleWidget.setLayout(QHBoxLayout())
        titleWidget.layout().addWidget(QLabel("GMini"))
        titleWidget.layout().addStretch()
        userLabel = ClickableLabel("Perfil")
        userLabel.clicked.connect(self.open_user_profile)
        titleWidget.layout().addWidget(userLabel)
        layout.addWidget(titleWidget)

        toolbar.addAction("Nueva sesion", self.nueva_sesion)
        toolbar.addAction("Graficas", self.graficas)
        # toolbar.addAction("Calibracion", self.calibracion)
        toolbar.addAction("Analisis", self.analisis)
        toolbar.addAction("Exportar", self.exportar)
        toolbar.addAction("Importar", self.importar)
        toolbar.addAction("Guardar", self.guardar)

        layout.addWidget(toolbar)
        layout.addWidget(mainWidget)
        mainWidget.setLayout(QHBoxLayout())

        leftWidget = QWidget()
        leftWidget.setFixedWidth(320)
        leftLayout = QVBoxLayout()
        leftWidget.setLayout(leftLayout)

        middleWidget = QWidget()
        middleWidget.setStyleSheet("background-color: #313244;")
        middleLayout = QVBoxLayout()
        middleWidget.setLayout(middleLayout)

        rightWidget = QWidget()
        rightWidget.setFixedWidth(320)
        rightLayout = QVBoxLayout()
        rightWidget.setLayout(rightLayout)

        mensaje = QLabel("¡Bienvenido a la Pantalla Principal!")
        mensaje.setAlignment(Qt.AlignmentFlag.AlignCenter)
        middleLayout.addWidget(mensaje)

        self.setLayout(layout)

        mainWidget.layout().addWidget(leftWidget,1)
        mainWidget.layout().addWidget(middleWidget,3)
        mainWidget.layout().addWidget(rightWidget,1)

        # Left widget
        dispositivoWidget = CollapseWidget("Dispositivo")
        dispositivoTab = QTabWidget()

        bluetoothTab = QWidget()
        bluetoothTab.setLayout(QVBoxLayout())
        bluetoothTab.layout().addWidget(QLabel("Guanaco MINI"))
        disconnectBtButton = QPushButton("Desconectar")
        disconnectBtButton.clicked.connect(self.desconectar)
        bluetoothTab.layout().addWidget(disconnectBtButton)

        usbTab = QWidget()
        usbTab.setLayout(QVBoxLayout())
        usbTab.layout().addWidget(QLabel("Guanaco MINI"))

        dispositivoTab.addTab(bluetoothTab, "Bluetooth")
        dispositivoTab.addTab(usbTab, "USB")
        dispositivoWidget.layout().addWidget(dispositivoTab)
        leftLayout.addWidget(dispositivoWidget)

        metodoWidget = CollapseWidget("Metodo de Medicion")
        espectroRadio = QRadioButton("Espectroscopia")
        espectroRadio.setChecked(True)
        monofreqRadio = QRadioButton("Monofrecuencia (Dom. tiempo)")
        multifreqTiempoRadio = QRadioButton("Multifrecuencia (Dom. tiempo)")
        multifreqFrecuenciaRadio = QRadioButton("Multifrecuencia (Dom. frecuencia)")
        metodoWidget.layout().addWidget(espectroRadio)
        metodoWidget.layout().addWidget(monofreqRadio)
        metodoWidget.layout().addWidget(multifreqTiempoRadio)
        metodoWidget.layout().addWidget(multifreqFrecuenciaRadio)
        leftLayout.addWidget(metodoWidget)

        parametrosWidget = CollapseWidget("Parametros")
        for i in range(5):
            parametrosWidget.layout().addWidget(TextBox(f"Parametro {i+1}"))
        leftLayout.addWidget(parametrosWidget)

        leftLayout.addStretch()

        # Right widget
        controlWidget = CollapseWidget("Control")
        iniciarButton = QPushButton("Iniciar medicion")
        iniciarButton.clicked.connect(self.iniciar)
        pararButton = QPushButton("Parar medicion")
        pararButton.clicked.connect(self.parar)
        controlWidget.layout().addWidget(iniciarButton)
        controlWidget.layout().addWidget(pararButton)
        rightLayout.addWidget(controlWidget)

        calibracionWidget = CollapseWidget("Calibracion")
        calibracionButton = QPushButton("Iniciar Calibracion")
        calibracionButton.clicked.connect(self.calibracion)
        calibracionWidget.layout().addWidget(calibracionButton)
        rightLayout.addWidget(calibracionWidget)

        historialWidget = CollapseWidget("Historial")
        historialWidget.layout().addWidget(QLabel("Contenido de Historial"))
        rightLayout.addWidget(historialWidget)
        
        rightLayout.addStretch()

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

    def iniciar(self):
        pass

    def parar(self):
        pass

    def desconectar(self):
        pass

    def open_user_profile(self):
        ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        if ruta_raiz not in sys.path:
            sys.path.append(ruta_raiz)
        from user_window.user_profile_window import UserProfileWindow
        self.userProfileWindow = UserProfileWindow()
        self.userProfileWindow.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())