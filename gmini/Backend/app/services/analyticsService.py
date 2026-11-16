import pyqtgraph as pg
import numpy as np
from typing import Dict, Any, Optional
from gmini.Backend.app.models.measure import Measure

class AnalyticsService:
    def plot_debye(self, result_data: list, plot_widget: pg.PlotWidget):
        """
        Recibe una lista de números complejos (impedancias)
        y grafica un diagrama de Nyquist/Debye (Real vs -Imag).
        Se divide por 1000 para normalizar la escala a kOhms.
        """
        # CORRECCIÓN: Uso .real e .imag en lugar de índices [0] y [1]
        real_values = [punto.real / 1000.0 for punto in result_data]
        imag_values = [-punto.imag / 1000.0 for punto in result_data] 
                 
        plot_widget.clear()
        plot_widget.setLabel('left', '-Imaginario', units='kΩ')
        plot_widget.setLabel('bottom', 'Real', units='kΩ')
        plot_widget.setTitle("Gráfico de Debye (Nyquist)")
        plot_widget.showGrid(x=True, y=True)
                 
        plot_widget.plot(real_values, imag_values, pen='c', symbol='o', symbolBrush='b')

    @staticmethod
    def calculate_basic_stats(measure: Measure) -> Dict[str, Any]:
        if measure.get_state() != 'COMPLETE':
            return {
                "error": "Los analíticos solo pueden realizarse sobre mediciones con estado COMPLETE."
            }
        
        result = measure.get_measure_result()
        if not result or not result.get_impedances():
            return {
                "error": "No hay datos de impedancia almacenados en el resultado."
            }
            
        imp_array = np.array(result.get_impedances())
        reals = imp_array.real
        imags = imp_array.imag
        magnitudes = np.abs(imp_array)
        phases = np.angle(imp_array)
        
        return {
            "imp_real_mean": float(np.mean(reals)),
            "imp_imag_mean": float(np.mean(imags)),
            "imp_real_std": float(np.std(reals)),
            "imp_imag_std": float(np.std(imags)),
            "imp_mod_mean": float(np.mean(magnitudes)),
            "imp_mod_max": float(np.max(magnitudes)),
            "imp_mod_min": float(np.min(magnitudes)),
            "imp_phase_max": float(np.max(phases)),
            "imp_phase_min": float(np.min(phases))
        }

    @staticmethod
    def calculate_impedance_at_frequency(measure: Measure, target_freq: float) -> Optional[complex]:
        if measure.get_state() != 'COMPLETE':
            return None
                     
        result = measure.get_measure_result()
        if not result:
            return None
            
        try:
            index = result.get_frequencies().index(target_freq)
            return result.get_impedances()[index]
        except ValueError:
            return None