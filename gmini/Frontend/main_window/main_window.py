from ast import main
import os,sys
import yaml
import pyqtgraph as pg
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QMenu,
    QFormLayout,
    QPushButton,
    QRadioButton,
    QTabWidget,
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QTableWidget, 
    QTableWidgetItem,
    QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal

from gmini.Backend.app.services.connectionService import ConnectionService
from gmini.Backend.app.services.calibrationService import CalibrationService
from gmini.Backend.app.services.measureService import MeasureService
from gmini.Backend.app.models.device import Device
from gmini.Backend.app.core.mock_connection import MockWire
from gmini.Backend.app.services.sessionManager import SessionManager
from gmini.Backend.app.adapters.gminiMeasureAdapter import GminiMeasureAdapter
from gmini.Backend.app.adapters.gminiCalibrationAdapter import GminiCalibrationAdapter
from gmini.Backend.app.db.databaseService import DataBaseService
from gmini.Backend.app.services.analyticsService import AnalyticsService # Tu nuevo servicio
from gmini.Frontend.user_window.user_profile_window import UserProfileWindow
from gmini.Backend.app.services.localServices import LocalService
from gmini.Backend.app.models.calibrationSetup import CalibrationSetup
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.parameter_boxes = {}
        self.local_service = LocalService()
        
        # 1. dispositivo
        self.device = Device(device_id=1)
        
        # 2. Servicios base 
        self.analytics_service = AnalyticsService()
        self.connection_service = ConnectionService()
        self.session_manager = SessionManager()
        self.db_service = DataBaseService()
        
        # 3. Instanciar los adaptadores que faltaban
        self.measure_adapter = GminiMeasureAdapter()
        self.calibration_adapter = GminiCalibrationAdapter()
        
        # 4. Servicios complejos ( dependencias inyectadas)
        self.calibration_service = CalibrationService(
            connection_service=self.connection_service, 
            adapter=self.calibration_adapter,           
            session_manager=self.session_manager
        )
        
        self.measure_service = MeasureService(
            connection_service=self.connection_service, 
            adapter=self.measure_adapter,               
            session_manager=self.session_manager,
            db_service=self.db_service
        )
        self.current_setup = None
        self.current_measure = None
        self.current_calibration_setup = None
        self.status_label = None
        self._applying_import = False
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e; color: #cdd6f4;
            }
        """)
        self.inicializar_ui()

    def inicializar_ui(self):
        self.setFixedSize(1280, 720)
        self.setWindowTitle("Pantalla Principal")

        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self._create_title_widget())
        central_layout.addWidget(self._create_main_widget())
        self.setCentralWidget(central_widget)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self._create_toolbar())

    def _create_title_widget(self):
        title_widget = QWidget()
        title_layout = QHBoxLayout()
        title_widget.setLayout(title_layout)
        title_layout.addWidget(QLabel("GMini"))
        title_layout.addStretch()

        user_label = ClickableLabel("Perfil")
        user_label.clicked.connect(self.open_user_profile)
        title_layout.addWidget(user_label)
        return title_widget

    def _create_toolbar(self):
        toolbar = QToolBar()
        toolbar.addAction("Nueva sesion", self.nueva_sesion)
        toolbar.addAction("Graficas", self.graficas)
        # toolbar.addAction("Calibracion", self.calibracion)
        toolbar.addAction("Analisis", self.analisis)
        toolbar.addWidget(
            self._create_toolbar_menu(
                "Exportar",
                ("Medicion", self.exportar_medicion),
                "Configuracion",
                (
                    ("Medicion", self.exportar_configuracion),
                    ("Calibracion", self.exportar_calibracion),
                ),
            )
        )
        toolbar.addWidget(
            self._create_toolbar_menu(
                "Importar",
                ("Medicion", self.importar_medicion),
                "Configuracion",
                (
                    ("Medicion", self.importar_configuracion),
                    ("Calibracion", self.importar_calibracion),
                ),
            )
        )
        toolbar.addAction("Guardar", self.guardar)
        return toolbar

    def _create_toolbar_menu(
        self, title, main_action, submenu_title, submenu_actions
    ):
        button = QToolButton()
        button.setText(title)
        button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        menu = QMenu(button)
        menu.addAction(*main_action)
        submenu = menu.addMenu(submenu_title)
        for action_text, callback in submenu_actions:
            submenu.addAction(action_text, callback)
        button.setMenu(menu)
        return button

    def _create_main_widget(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        left_widget, left_layout = self._create_panel(width=320)
        middle_widget, middle_layout = self._create_panel(
            style="background-color: #313244;"
        )
        right_widget, right_layout = self._create_panel(width=320)

        self.status_label = QLabel("Bienvenido a la Pantalla Principal!")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFixedHeight(35)
        self.status_label.setStyleSheet("background-color: #45475a; border-radius: 5px; font-weight: bold;")
        
        # --- NUEVO: CONTENEDOR DE PESTAÑAS (TABS) ---
        self.results_tabs = QTabWidget()
        self.results_tabs.hide() # Lo ocultamos hasta medir
        self.results_tabs.setStyleSheet("QTabWidget::pane { border: 1px solid #45475a; }")

        # 1. Pestaña del Gráfico
        tab_grafico = QWidget()
        layout_grafico = QVBoxLayout(tab_grafico)
        layout_grafico.setContentsMargins(0, 0, 0, 0)
        
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#1e1e2e')
        layout_grafico.addWidget(self.plot_widget)
        self.results_tabs.addTab(tab_grafico, "Gráfico (Nyquist)")

        # 2. Pestaña de la Tabla de Datos
        tab_tabla = QWidget()
        layout_tabla = QVBoxLayout(tab_tabla)
        layout_tabla.setContentsMargins(0, 0, 0, 0)
        
        self.data_table = QTableWidget()
        self.data_table.setStyleSheet("background-color: #1e1e2e; gridline-color: #45475a;")
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout_tabla.addWidget(self.data_table)
        self.results_tabs.addTab(tab_tabla, "Datos Crudos")

        # Agregamos al layout central
        middle_layout.addWidget(self.status_label)
        middle_layout.addWidget(self.results_tabs)
        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(middle_widget, 3)
        main_layout.addWidget(right_widget, 1)

        self._populate_left_panel(left_layout)
        self._populate_right_panel(right_layout)
        return main_widget

    @staticmethod
    def _create_panel(width=None, style=None):
        panel = QWidget()
        if width is not None:
            panel.setFixedWidth(width)
        if style is not None:
            panel.setStyleSheet(style)
        panel_layout = QVBoxLayout()
        panel.setLayout(panel_layout)
        return panel, panel_layout

    def _populate_left_panel(self, layout):
        layout.addWidget(self._create_device_widget())
        layout.addWidget(self._create_measure_method_widget())
        layout.addWidget(self._create_parameters_widget())
        layout.addStretch()

    def _create_device_widget(self):
        device_widget = CollapseWidget("Dispositivo")
        device_tabs = QTabWidget()

        bluetooth_tab = QWidget()
        bluetooth_layout = QVBoxLayout()
        bluetooth_tab.setLayout(bluetooth_layout)
        bluetooth_layout.addWidget(QLabel("Guanaco MINI"))
        self.btn_conectar_desconectar = QPushButton("Conectar")
        self.btn_conectar_desconectar.clicked.connect(self.desconectar)
        bluetooth_layout.addWidget(self.btn_conectar_desconectar)

        usb_tab = QWidget()
        usb_layout = QVBoxLayout()
        usb_tab.setLayout(usb_layout)
        usb_layout.addWidget(QLabel("Guanaco MINI"))

        device_tabs.addTab(bluetooth_tab, "Bluetooth")
        device_tabs.addTab(usb_tab, "USB")
        device_widget.layout().addWidget(device_tabs)
        return device_widget

    def _create_measure_method_widget(self):
        method_widget = CollapseWidget("Metodo de Medicion")
        radios = (
            QRadioButton("Espectroscopia"),
            QRadioButton("Monofrecuencia (Dom. tiempo)"),
            QRadioButton("Multifrecuencia (Dom. tiempo)"),
            QRadioButton("Multifrecuencia (Dom. frecuencia)"),
        )
        radios[0].setChecked(True)
        for radio in radios:
            method_widget.layout().addWidget(radio)
        self.measure_method_radios = radios
        return method_widget

    def _create_parameters_widget(self):
        parameters_widget = CollapseWidget("Parametros")
        self.parameter_layout = QFormLayout()
        parameters_widget.layout().addLayout(self.parameter_layout)
        for radio in self.measure_method_radios:
            radio.toggled.connect(self._update_measure_parameters)
        self._update_measure_parameters()
        return parameters_widget

    def _populate_right_panel(self, layout):
        control_widget = CollapseWidget("Control")
        start_button = QPushButton("Iniciar medicion")
        start_button.clicked.connect(self.iniciar)
        stop_button = QPushButton("Parar medicion")
        stop_button.clicked.connect(self.parar)
        control_widget.layout().addWidget(start_button)
        control_widget.layout().addWidget(stop_button)
        layout.addWidget(control_widget)

        calibration_widget = CollapseWidget("Calibracion")
        calibration_widget.layout().addWidget(
            self._create_calibration_parameters_widget()
        )
        calibration_button = QPushButton("Iniciar Calibracion")
        calibration_button.clicked.connect(self.calibracion)
        calibration_widget.layout().addWidget(calibration_button)
        layout.addWidget(calibration_widget)

        history_widget = CollapseWidget("Historial")
        history_widget.layout().addWidget(QLabel("Contenido de Historial"))
        layout.addWidget(history_widget)
        layout.addStretch()

    def nueva_sesion(self):
        pass

    def graficas(self):
        pass

    def calibracion(self):
        # Verificamos si hay conexión antes de intentar calibrar
        if not self.connection_service.active_connections.get(self.device.get_id()):
            self._show_error("Error", "Debe conectar el dispositivo primero.")
            return

        try:
            self.current_calibration_setup = self.get_calibration_setup()
            self.current_measure = None
            
            # Llamamos al servicio para ejecutar la calibración en el hardware simulado
            self.calibration_service.calibrate_device(self.device, self.current_calibration_setup)
            
            # El estado interno del 'device' pasará a CalibratedState.
            self._show_status("Placa calibrada correctamente.")
            
        except ValueError as exc:
            self._show_error("Calibracion", str(exc))
        except Exception as e:
            self._show_error("Error de Hardware", f"Fallo al calibrar: {str(e)}")

    def _create_calibration_parameters_widget(self):
        parameters_widget = QWidget()
        self.calibration_parameter_layout = QFormLayout()
        parameters_widget.setLayout(self.calibration_parameter_layout)
        self.calibration_parameter_boxes = {}

        parameters = (
            ("channel", "Canal"),
            ("z_calc_value_real", "Valor Z calculado real"),
            ("z_calc_value_imag", "Valor Z calculado imaginario"),
            ("exitation_voltage", "Voltaje de excitacion"),
            ("gain", "Ganancia"),
            ("rfbvalue", "Valor RFB"),
            ("settcycles", "Ciclos de estabilizacion"),
            ("mux_channel", "Canales MUX"),
            ("observations", "Observaciones"),
        )
        for name, label in parameters:
            box = QLineEdit()
            box.setStyleSheet("background-color: #45475a;")
            self.calibration_parameter_layout.addRow(label, box)
            self.calibration_parameter_boxes[name] = box
        return parameters_widget

    def analisis(self):
        pass

    def exportar_medicion(self):
        if self.current_measure is None:
            self._show_error("Exportar medicion", "No hay una medicion para exportar")
            return
        self._export_to_file(
            "Exportar medicion",
            "medicion.yaml",
            self.local_service.export_measure_to_file,
            self.current_measure,
        )

    def exportar_calibracion(self):
        try:
            self.current_calibration_setup = self.get_calibration_setup()
        except ValueError as exc:
            self._show_error("Exportar calibracion", str(exc))
            return
        self._export_to_file(
            "Exportar calibracion",
            "calibracion_config.yaml",
            self.local_service.export_calibration_setup_to_file,
            self.current_calibration_setup,
        )

    def exportar_configuracion(self):
        try:
            self.current_setup = self.get_measure_setup()
        except ValueError as exc:
            self._show_error("Exportar configuracion", str(exc))
            return
        self._export_to_file(
            "Exportar configuracion",
            "medicion_config.yaml",
            self.local_service.export_setup_to_file,
            self.current_setup,
        )

    def _export_to_file(self, title, default_name, exporter, value):
        path, _ = QFileDialog.getSaveFileName(
            self,
            title,
            default_name,
            "Archivos YAML (*.yaml *.yml);;Todos los archivos (*)",
        )
        if not path:
            return

        try:
            exporter(path, value)
        except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
            self._show_error(title, f"No se pudo exportar el archivo:\n{exc}")
            return
        self._show_status(f"Archivo exportado: {path}")

    def importar_medicion(self):
        self._import_from_file(
            "Importar medicion",
            self.local_service.load_measure,
            self._apply_imported_measure,
        )

    def importar_calibracion(self):
        self._import_from_file(
            "Importar calibracion",
            self.local_service.load_calibration_setup,
            self._apply_imported_calibration,
        )

    def importar_configuracion(self):
        self._import_from_file(
            "Importar configuracion",
            self.local_service.load_setup,
            self._apply_imported_setup,
        )

    def _import_from_file(self, title, importer, apply_import):
        path, _ = QFileDialog.getOpenFileName(
            self,
            title,
            "",
            "Archivos YAML (*.yaml *.yml);;Todos los archivos (*)",
        )
        if not path:
            return

        try:
            value = importer(path)
            apply_import(value)
        except (OSError, ValueError, TypeError) as exc:
            self._show_error(title, f"No se pudo importar el archivo:\n{exc}")
            return
        self._show_status(f"Archivo importado: {path}")

    def _apply_imported_measure(self, measure):
        self.current_measure = measure
        self.current_setup = measure.get_measure_setup()
        self.current_calibration_setup = None
        self._apply_measure_setup(self.current_setup)

    def _apply_imported_calibration(self, calibration_setup):
        self.current_calibration_setup = calibration_setup
        self.current_measure = None
        self._apply_calibration_setup(calibration_setup)

    def _apply_imported_setup(self, setup):
        self.current_setup = setup
        self.current_measure = None
        self.current_calibration_setup = None
        self._apply_measure_setup(setup)

    def _apply_calibration_setup(self, setup):
        values = {
            "channel": setup.get_channel(),
            "z_calc_value_real": setup.get_z_calc_value_real(),
            "z_calc_value_imag": setup.get_z_calc_value_imag(),
            "exitation_voltage": setup.get_exitation_voltage(),
            "gain": setup.get_gain(),
            "rfbvalue": setup.get_rfbvalue(),
            "settcycles": setup.get_settcycles(),
            "mux_channel": ", ".join(map(str, setup.get_mux_channel())),
            "observations": setup.get_observations(),
        }
        for name, value in values.items():
            self.calibration_parameter_boxes[name].setText(str(value))

    def guardar(self):
        pass

    def iniciar(self):
        # La Vista solo verifica que exista el enlace de comunicación
        if not self.connection_service.active_connections.get(self.device.get_id()):
            self._show_error("Error", "Debe conectar el dispositivo primero.")
            return
            
        try:
            # 1. Recolectar datos de la GUI
            setup = self.get_measure_setup()
            
            # 2. Envolver el setup en la entidad Measure (importación y creación correctas)
            from gmini.Backend.app.models.measure import Measure
            
            # Instanciamos usando los nombres exactos que pide tu clase
            nueva_medicion = Measure(measure_setup=setup, device_id=self.device.device_id)
            
            self._show_status("Delegando medición al servicio...")
            
            # 3. Llamamos al orquestador
            self.measure_service.execute_measure(self.device, nueva_medicion)
            
            self._show_status("Medición ejecutada y finalizada correctamente.")

            # --- NUEVA LÓGICA DE GRÁFICOS Y TABLAS ---
            self.results_tabs.show() # Mostramos las solapas
            
            datos_de_prueba = [[185, -1830], [634, -1717]] 
            
            # 1. Actualizamos el gráfico
            self.analytics_service.plot_debye(datos_de_prueba, self.plot_widget)
            
            # 2. Actualizamos la tabla
            self._actualizar_tabla_datos(datos_de_prueba)
            # ---------------------------------------------
            
        except ValueError as exc:
            self._show_error("Error de configuración", str(exc))
        except RuntimeError as exc:
            # Atrapa el bloqueo de "No calibrado" que lanza el MeasureService
            self._show_error("Bloqueo de Seguridad", str(exc))
        except PermissionError as exc:
            # Atrapa el bloqueo de "Sin sesión" que lanza el MeasureService
            self._show_error("Error de Sesión", str(exc))
        except Exception as e:
            self._show_error("Error Interno", str(e))

    def parar(self):
        pass

    def desconectar(self):
    # Esta funcion actuara como "Toggle" (Conectar/Desconectar)
        if not self.connection_service.active_connections.get(self.device.get_id()):
            # Conectar usando el MockWire simulado
            mock_wire = MockWire()
            self.connection_service.connect(self.device, mock_wire)
        
            # Cambiar texto del boton a "Desconectar"
            self.btn_conectar_desconectar.setText("Desconectar")
        
            self._show_status("Conectado exitosamente al simulador ESP32.")
        else:
            # Desconectar
            self.connection_service.disconnect(self.device)
        
            # Cambiar texto del boton a "Conectar"
            self.btn_conectar_desconectar.setText("Conectar")
        
            self._show_status("Dispositivo desconectado.")

    def open_user_profile(self):
        self.profile_window = UserProfileWindow(self) 
        self.profile_window.show()
        self.hide() 

    def _apply_measure_setup(self, setup):
        self._applying_import = True
        try:
            if isinstance(setup, SpecMeasureSetup):
                self.measure_method_radios[0].setChecked(True)
                values = {
                    "startfreq": str(setup.get_start_freq()),
                    "incfreq": str(setup.get_inc_freq()),
                    "steps": str(setup.get_steps()),
                    "repeat": str(setup.get_repeat()),
                }
            elif isinstance(setup, SingleMeasureSetup):
                self.measure_method_radios[1].setChecked(True)
                values = {
                    "freq": setup.freq,
                    "delay": setup.delay,
                    "count": setup.count,
                }
            elif isinstance(setup, MultiMeasureSetup):
                self.measure_method_radios[2].setChecked(True)
                values = {"freq_list": ", ".join(map(str, setup.freq_list))}
            else:
                raise ValueError(
                    f"Tipo de configuración no soportado: {type(setup).__name__}"
                )

            for name, value in values.items():
                self.parameter_boxes[name].setText(str(value))
        finally:
            self._applying_import = False

    def _show_status(self, message):
        if self.status_label is not None:
            self.status_label.setText(message)

    def _show_error(self, title, message):
        QMessageBox.critical(self, title, message)

    def _update_measure_parameters(self):
        if not self._applying_import:
            self.current_measure = None
            self.current_calibration_setup = None
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

    def get_calibration_setup(self) -> CalibrationSetup:
        try:
            channel = self.calibration_parameter_boxes["channel"].text().strip()
            if not channel:
                raise ValueError("El canal de calibracion no puede estar vacio")
            
            # --- NUEVA LÓGICA ---
            mux_channel_str = self.calibration_parameter_boxes["mux_channel"].text().strip()
            if not mux_channel_str:
                raise ValueError("Debe indicar el canal MUX")
            mux_channel_int = int(mux_channel_str)
            # ---------------------------------------

            setup = CalibrationSetup(
                channel=channel,
                z_calc_value_real=float(self.calibration_parameter_boxes["z_calc_value_real"].text()),
                z_calc_value_imag=float(self.calibration_parameter_boxes["z_calc_value_imag"].text()),
                exitation_voltage=float(self.calibration_parameter_boxes["exitation_voltage"].text()),
                gain=float(self.calibration_parameter_boxes["gain"].text()),
                rfbvalue=float(self.calibration_parameter_boxes["rfbvalue"].text()),
                settcycles=int(self.calibration_parameter_boxes["settcycles"].text()),
                mux_channel=mux_channel_int, # <--- Pasamos el entero directo
            )
            setup.set_observations(self.calibration_parameter_boxes["observations"].text())
            return setup
        
        except ValueError as exc:
            if str(exc) in {
                "El canal de calibracion no puede estar vacio",
                "Debe indicar al menos un canal MUX",
            }:
                raise
            raise ValueError(
                "Los parámetros de calibracion no son válidos"
            ) from exc

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

    def _actualizar_tabla_datos(self, datos):
        # Configuramos filas y columnas
        self.data_table.setRowCount(len(datos))
        self.data_table.setColumnCount(2)
        self.data_table.setHorizontalHeaderLabels(["Parte Real (Ω)", "Parte Imaginaria (Ω)"])
        
        # Llenamos la tabla iterando sobre la lista
        for fila, punto in enumerate(datos):
            real_item = QTableWidgetItem(str(punto[0]))
            real_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            imag_item = QTableWidgetItem(str(punto[1]))
            imag_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.data_table.setItem(fila, 0, real_item)
            self.data_table.setItem(fila, 1, imag_item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())