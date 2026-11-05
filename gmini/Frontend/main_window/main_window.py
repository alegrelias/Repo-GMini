from ast import main
import os,sys
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QFormLayout,
    QPushButton,
    QRadioButton,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt, pyqtSignal

from gmini.Frontend.user_window.user_profile_window import UserProfileWindow
from gmini.Backend.app.models.measureSetup import (
    MeasureSetup,
    MultiMeasureSetup,
    SingleMeasureSetup,
    SpecMeasureSetup,
)


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
        self.parameter_boxes = {}
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
        self.parameter_layout = QFormLayout()
        parametrosWidget.layout().addLayout(self.parameter_layout)
        self.measure_method_radios = (
            espectroRadio,
            monofreqRadio,
            multifreqTiempoRadio,
            multifreqFrecuenciaRadio,
        )
        for radio in self.measure_method_radios:
            radio.toggled.connect(self._update_measure_parameters)
        self._update_measure_parameters()
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
        self.userProfileWindow = UserProfileWindow()
        self.userProfileWindow.show()

    def _update_measure_parameters(self):
        selected_radio = next(
            (radio for radio in self.measure_method_radios if radio.isChecked()),
            None,
        )
        if selected_radio is None:
            return

        if selected_radio.text() == "Espectroscopia":
            parameters = (
                ("startfreq", "Frecuencia inicial"),
                ("incfreq", "Incremento de frecuencia"),
                ("steps", "Pasos"),
                ("repeat", "Repeticiones"),
            )
        elif selected_radio.text() == "Monofrecuencia (Dom. tiempo)":
            parameters = (
                ("freq", "Frecuencia"),
                ("delay", "Retardo"),
                ("count", "Repeticiones"),
            )
        else:
            parameters = (("freq_list", "Frecuencias (separadas por comas)"),)

        while self.parameter_layout.count():
            item = self.parameter_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        self.parameter_boxes = {}
        for name, label in parameters:
            box = QLineEdit()
            box.setStyleSheet("background-color: #45475a;")
            self.parameter_layout.addRow(label, box)
            self.parameter_boxes[name] = box

    def get_measure_setup(self) -> MeasureSetup:
        selected_radio = next(
            (radio for radio in self.measure_method_radios if radio.isChecked()),
            None,
        )
        if selected_radio is None:
            raise ValueError("Debe seleccionar un método de medición")

        try:
            if selected_radio.text() == "Espectroscopia":
                return SpecMeasureSetup(
                    startfreq=float(self.parameter_boxes["startfreq"].text()),
                    incfreq=float(self.parameter_boxes["incfreq"].text()),
                    steps=int(self.parameter_boxes["steps"].text()),
                    repeat=int(self.parameter_boxes["repeat"].text()),
                )
            if selected_radio.text() == "Monofrecuencia (Dom. tiempo)":
                return SingleMeasureSetup(
                    freq=float(self.parameter_boxes["freq"].text()),
                    delay=int(self.parameter_boxes["delay"].text()),
                    count=int(self.parameter_boxes["count"].text()),
                )
            frequencies = [
                float(value.strip())
                for value in self.parameter_boxes["freq_list"].text().split(",")
                if value.strip()
            ]
            if not frequencies:
                raise ValueError("La lista de frecuencias no puede estar vacía")
            return MultiMeasureSetup(freq_list=frequencies)
        except ValueError as exc:
            raise ValueError("Los parámetros de medición no son válidos") from exc


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())