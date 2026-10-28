import sys 
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,QLabel, QPushButton, QTabWidget, QScrollArea, QFrame,QSizePolicy, QMessageBox)
from PyQt6.QtCore import Qt

class Historial_fila(QFrame): 
    def __init__(self, item_id: int, nombre: str, fecha: str, estado: str, parent=None):
        super().__init__(parent)
        self.item_id = item_id
        self.nombre = nombre
        self.setObjectName("FilaHistorial")
        self.setFixedHeight(52)

        #contenedor horisontal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 6, 15, 6)
        layout.setSpacing(15)

        #icono de documento y nombre
        self.icono_label = QLabel("📄")
        self.icono_label.setStyleSheet("font-size: 18px; background: transparent; border: none;")

        self.nombre_label = QLabel(nombre)
        self.nombre_label.setStyleSheet("color: #EAEAEA; font-size: 15px; background: transparent; border: none;")
        self.nombre_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.fecha_label = QLabel(fecha)
        self.fecha_label.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: bold; background: transparent; border: none;")
        self.fecha_label.setFixedWidth(160)
        self.fecha_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #colores de estados
        self.estado_label = QLabel(estado)
        color_estado = "#4CAF50" if estado.lower() == "completado" else "#9EA4B0"
        self.estado_label.setStyleSheet(f"color: {color_estado}; font-size: 15px; background: transparent; border: none;")
        self.estado_label.setFixedWidth(110)
        self.estado_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #boton de abrir 
        self.btn_abrir = QPushButton("📁")
        self.btn_abrir.setObjectName("btnAbrir")
        self.btn_abrir.setFixedSize(36, 32)
        self.btn_abrir.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_abrir.setToolTip("Cargar / Visualizar")

        #boton de eliminar
        self.btn_eliminar = QPushButton("🗑️")
        self.btn_eliminar.setObjectName("btnEliminar")
        self.btn_eliminar.setFixedSize(36, 32)
        self.btn_eliminar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_eliminar.setToolTip("Eliminar registro")

        #agregar componentes
        layout.addWidget(self.icono_label)
        layout.addWidget(self.nombre_label)
        layout.addWidget(self.fecha_label)
        layout.addWidget(self.estado_label)
        layout.addWidget(self.btn_abrir)
        layout.addWidget(self.btn_eliminar)


class UserMeasuresAndSetupsWindow(QWidget):
    def __init__(self, ventana_principal=None):
        super().__init__()
        self.ventana_principal = ventana_principal
        self.inicializar_ui()

    def inicializar_ui(self):
        self.setWindowTitle("GMini GUI")
        self.resize(980, 560)
        self.setStyleSheet("""
            QWidget {
                background-color: #1E2024;
                color: white;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel#tituloHeader {
                color: #D8DEE9;
                font-size: 32px;
            }
            QTabWidget::pane {
                border: 2px solid #3E424B;
                border-radius: 8px;
                background-color: #1A1C20;
                top: -1px;
            }
            QTabBar::tab {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #434750, stop:1 #2B2E34);
                color: #CCCCCC;
                border: 1px solid #4A4E57;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                min-width: 280px;
                padding: 8px 15px;
                font-size: 15px;
                margin-right: 4px;
            }
            QTabBar::tab:selected {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2B5B6C, stop:1 #1D3540);
                color: #FFFFFF;
                border: 1px solid #4F94CD;
                border-bottom: none;
            }
            QFrame#FilaHistorial {
                border-bottom: 1px solid #32363E;
                background-color: transparent;
            }
            QFrame#FilaHistorial:hover {
                background-color: #262930;
            }
            QPushButton#btnAbrir, QPushButton#btnEliminar {
                background-color: #3A3F47;
                border: 1px solid #525863;
                border-radius: 6px;
                font-size: 15px;
            }
            QPushButton#btnAbrir:hover {
                background-color: #3a6085;
                border-color: #5CA4EA;
            }
            QPushButton#btnEliminar:hover {
                background-color: #6C2B2B;
                border-color: #EA5C5C;
            }
            QScrollBar:vertical {
                background: #1A1C20;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4C525C;
                min-height: 30px;
                border-radius: 5px;
            }
        """)

        self.generar_interfaz()

    def generar_interfaz(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 20)
        main_layout.setSpacing(10)

        #cabecera Superior 
        top_layout = QHBoxLayout()
        title_label = QLabel("GMini GUI")
        title_label.setObjectName("tituloHeader")
        owner_label = QLabel("LEAB")
        owner_label.setObjectName("tituloHeader")

        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addWidget(owner_label)
        main_layout.addLayout(top_layout)

        #Pestañas
        self.tabs = QTabWidget()

        #Datos de ejemplo (eliminar despues)
        mediciones_mock = [
            (145, "Medición #145 - Espectroscopia de prueba", "08/10/2026 14:15", "Completado"),
            (144, "Medición #144 - Muestra A", "07/10/2026 18:30", "Completado"),
            (143, "Medición #143 - Muestra B", "07/10/2026 09:32", "Guardado"),
            (142, "Medición #142 - Espectroscopia de calibración", "06/10/2026 16:48", "Completado"),
            (141, "Medición #141 - Muestra C", "05/10/2026 12:10", "Completado"),
            (140, "Medición #140 - Espectroscopia de prueba 2", "05/10/2026 10:15", "Guardado"),
            (139, "Medición #139 - Análisis de ruido", "04/10/2026 15:44", "Completado"),
            (138, "Medición #138 - Muestra D", "03/10/2026 11:20", "Guardado"),
        ]

        setups_cal_mock = [
            (1, "Setup Calibración #1 - RCAL1 100 Ohm", "02/10/2026 10:00", "Guardado"),
        ]

        setups_med_mock = [
            (1, "Setup Barrido Espectral 1kHz - 100kHz", "01/10/2026 16:20", "Guardado"),
        ]

        self.tab_mediciones = self.crear_pestana_lista(mediciones_mock)
        self.tab_setup_cal = self.crear_pestana_lista(setups_cal_mock)
        self.tab_setup_med = self.crear_pestana_lista(setups_med_mock)

        self.tabs.addTab(self.tab_mediciones, "Mediciones")
        self.tabs.addTab(self.tab_setup_cal, "Setup Calibraciones")
        self.tabs.addTab(self.tab_setup_med, "Setup Mediciones")

        main_layout.addWidget(self.tabs)

    def crear_pestana_lista(self, registros: list) -> QWidget:
        contenedor = QFrame()
        layout = QVBoxLayout(contenedor)
        layout.setContentsMargins(15, 10, 10, 10)
        layout.setSpacing(4)

        #marcador de fecha de creacion
        sub_header = QHBoxLayout()
        sub_header.addStretch()
        lbl_fecha = QLabel("Fecha de creación")
        lbl_fecha.setStyleSheet("color: #CFCFCF; font-size: 14px; background: transparent;")
        lbl_fecha.setFixedWidth(160)
        lbl_fecha.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_header.addWidget(lbl_fecha)
        sub_header.addSpacing(225)
        layout.addLayout(sub_header)

        #area de desplazamiento(scroll)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        contenido_scroll = QWidget()
        contenido_scroll.setStyleSheet("background: transparent;")
        filas_layout = QVBoxLayout(contenido_scroll)
        filas_layout.setContentsMargins(0, 0, 5, 0)
        filas_layout.setSpacing(0)

        for item_id, nombre, fecha, estado in registros:
            fila = Historial_fila(item_id, nombre, fecha, estado)
            fila.btn_abrir.clicked.connect(lambda checked, n=nombre: self.abrir_registro(n))
            fila.btn_eliminar.clicked.connect(lambda checked, f=fila, n=nombre: self.eliminar_registro(f, n))
            filas_layout.addWidget(fila)

        filas_layout.addStretch()
        scroll.setWidget(contenido_scroll)
        layout.addWidget(scroll)

        return contenedor

    def abrir_registro(self, nombre: str):
        QMessageBox.information(self, "Cargar registro", f"Abriendo: {nombre}")

    def eliminar_registro(self, widget_fila: QWidget, nombre: str):
        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar '{nombre}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if respuesta == QMessageBox.StandardButton.Yes:
            widget_fila.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = UserMeasuresAndSetupsWindow()
    ventana.show()
    sys.exit(app.exec())