import numpy as np
import pandas as pd
from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Backend.app.core.observer import IObserver, IObservable
from Backend.app.models.measure import Measure
from Backend.app.models.measureResult import MeasureResult

"""Renderiza el Módulo de Impedancia |Z| automáticamente:
    1. Al finalizar una lectura de 'sweep' o 'singlefreq' (vía IObserver).
    2. Al abrir una 'Measure' guardada en BD o archivo local (vía plot_from_measure)."""
class ImpedancePlotWidget(QWidget, IObserver):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._active_measure: Optional[Measure] = None
        self._df_current: Optional[pd.DataFrame] = None
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)

        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        self.lbl_summary = QLabel("Gráfica lista. Ejecute un sweep/singlefreq o abra una medición.")
        layout.addWidget(self.canvas)
        layout.addWidget(self.lbl_summary)

        self._draw_empty_axes()

    def _draw_empty_axes(self) -> None:
        self.ax.clear()
        self.ax.set_title("Módulo de Impedancia |Z|")
        self.ax.set_xlabel("Frecuencia [Hz]")
        self.ax.set_ylabel("Módulo de Impedancia |Z| [Ω]")
        self.ax.grid(True, linestyle="--", alpha=0.6)
        self.canvas.draw()

    """Transforma un MeasureResult en un DataFrame de Pandas con las columnas:sample_index, frequency_hz, real_ohm, imag_ohm, magnitude_ohm, phase_rad"""
    @staticmethod
    def build_dataframe(result: MeasureResult) -> pd.DataFrame:
        imp_array = np.asarray(result.get_impedances(), dtype=complex).ravel()
        freq_array = np.asarray(result.get_frequencies(), dtype=float).ravel()

        n_imps = len(imp_array)
        n_freqs = len(freq_array)

        if n_freqs == 1 and n_imps > 1:
            freq_array = np.full(n_imps, freq_array[0], dtype=float)
        elif n_freqs == 0 and n_imps > 0:
            freq_array = np.zeros(n_imps, dtype=float)
        elif n_freqs != n_imps:
            min_len = min(n_freqs, n_imps)
            freq_array = freq_array[:min_len]
            imp_array = imp_array[:min_len]

        df = pd.DataFrame({
            "sample_index": np.arange(1, len(imp_array) + 1),
            "frequency_hz": freq_array,
            "real_ohm": imp_array.real,
            "imag_ohm": imp_array.imag,
            "magnitude_ohm": np.abs(imp_array),
            "phase_rad": np.angle(imp_array)
        })
        return df

    """Recibe un objeto Measure (recién ejecutado o abierto desde BD/archivo), procesa sus datos con Pandas y renderiza el Módulo de Impedancia |Z|."""
    def plot_from_measure(self, measure: Measure) -> Optional[pd.DataFrame]:
        self._active_measure = measure
        result = measure.get_measure_result()

        if not result or len(result.get_impedances()) == 0:
            self._draw_empty_axes()
            self.lbl_summary.setText("La medición seleccionada no contiene datos de impedancia.")
            return None

        df = self.build_dataframe(result)
        self._df_current = df

        if df.empty:
            self._draw_empty_axes()
            return None

        self.ax.clear()
        title_name = measure.get_file_name() or "Medición Actual"

        #Distinguimos entre Barrido Espectral  y Monofrecuencia 
        is_single_freq = df["frequency_hz"].nunique() <= 1

        if is_single_freq:
            freq_val = float(df["frequency_hz"].iloc[0])
            self.ax.plot(
                df["sample_index"],
                df["magnitude_ohm"],
                marker="o",
                markersize=8,
                linestyle="-" if len(df) > 1 else "None",
                color="#d95f02",
                label=f"|Z| @ {freq_val:.1f} Hz"
            )
            self.ax.set_title(f"Monofrecuencia ({freq_val:.1f} Hz) - {title_name}")
            self.ax.set_xlabel("Muestra #")
            self.ax.set_xticks(df["sample_index"])
        else:
            df_sorted = df.sort_values(by="frequency_hz")
            self.ax.plot(
                df_sorted["frequency_hz"],
                df_sorted["magnitude_ohm"],
                marker="o",
                linestyle="-",
                color="#1f77b4",
                label="Módulo |Z| (Ω)"
            )
            self.ax.set_title(f"Barrido de Impedancia |Z| vs Frecuencia - {title_name}")
            self.ax.set_xlabel("Frecuencia [Hz]")

        self.ax.set_ylabel("Módulo de Impedancia |Z| [Ω]")
        self.ax.grid(True, linestyle="--", alpha=0.6)
        self.ax.legend()
        self.figure.tight_layout()
        self.canvas.draw()

        self.lbl_summary.setText(
            f"<b>Muestras:</b> {len(df)} | "
            f"<b>|Z| Medio:</b> {df['magnitude_ohm'].mean():.2f} Ω | "
            f"<b>|Z| Mín:</b> {df['magnitude_ohm'].min():.2f} Ω | "
            f"<b>|Z| Máx:</b> {df['magnitude_ohm'].max():.2f} Ω"
        )
        return df

    def set_watching_measure(self, measure: Measure) -> None:
        self._active_measure = measure

    def update(self, observable: IObservable, event_info: str) -> None:
        if event_info == "MEASURE_COMPLETED" and self._active_measure:
            self.plot_from_measure(self._active_measure)

    def get_current_dataframe(self) -> Optional[pd.DataFrame]:
        return self._df_current

    def get_figure(self) -> Figure:
        return self.figure