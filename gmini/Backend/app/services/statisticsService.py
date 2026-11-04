import numpy as np
from typing import Dict, Any, Optional
from app.models.measure import Measure

"""Servicio de dominio encargado de realizar todos los cálculos analíticos y estadísticos sobre los resultados brutos de las mediciones de bioimpedancia"""
class StatisticsService:
    @staticmethod
    def calculate_basic_stats(measure: Measure) -> Dict[str, Any]:
        # Regla de negocio: Solo se procesan mediciones completas
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