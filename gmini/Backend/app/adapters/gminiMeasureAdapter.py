import json
from gmini.Backend.app.adapters.iMeasureAdapter import IMeasureAdapter
from gmini.Backend.app.models.measureSetup import (
    MeasureSetup, SingleMeasureSetup, SpecMeasureSetup, MultiMeasureSetup
)
from gmini.Backend.app.models.measureResult import MeasureResult

"""Adaptador concreto para codificar ejecuciones de medición y decodificar"""
class GminiMeasureAdapter(IMeasureAdapter):
    def encode_execution(self, setup: MeasureSetup) -> str:
        if isinstance(setup, SingleMeasureSetup):
            freq = setup.get_freq()
            delay = setup.get_delay() if hasattr(setup, "get_delay") else getattr(setup, "_delay", 0)
            count = (
                setup.get_count() if hasattr(setup, "get_count")
                else getattr(setup, "_count", getattr(setup, "_repeat", 1))
            )
            if delay > 0 or count > 1:
                return f"singlefreq {freq} {delay} {count}\n"
            return f"singlefreq {freq} {count}\n"

        elif isinstance(setup, SpecMeasureSetup):
            return (
                f"sweep {setup.get_start_freq()} "
                f"{setup.get_inc_freq()} "
                f"{setup.get_steps()} "
                f"{setup.get_repeat()}\n"
            )

        elif isinstance(setup, MultiMeasureSetup):
            commands = [f"singlefreq {freq} 0 1" for freq in setup.get_freq_list()]
            return "\n".join(commands) + "\n"

        else:
            raise ValueError(f"Tipo de MeasureSetup no soportado: {type(setup)}")

    def decode(self, raw_data: str) -> MeasureResult:
        try:
            # 1. Limpiamos la basura de la terminal serial
            clean_str = raw_data.replace("ad5933>", "").strip()
            
            if clean_str.lower().startswith("json"):
                clean_str = clean_str[4:].strip()

            # 2. Intentamos leerlo como JSON
            try:
                data = json.loads(clean_str)

                if "impedance" in data and "frequency" in data:
                    frequencies = [float(f) for f in data["frequency"]]
                    impedances = [complex(float(pair[0]), float(pair[1])) for pair in data["impedance"]]
                    # CORRECCIÓN: Se agregan amplitudes y phases vacíos
                    return MeasureResult(frequencies=frequencies, amplitudes=[], phases=[], impedances=impedances)

                if "sweep" in data:
                    res_block = data["sweep"].get("result", {})
                    frequencies = [float(f) for f in res_block.get("frequency", [])]
                    impedances = [complex(float(pair[0]), float(pair[1])) for pair in res_block.get("magnitude", [])]
                    # CORRECCIÓN: Se agregan amplitudes y phases vacíos
                    return MeasureResult(frequencies=frequencies, amplitudes=[], phases=[], impedances=impedances)

                frequencies = [float(f) for f in data.get("frequencies", [])]
                reals = data.get("reals", [])
                imags = data.get("imags", [])
                impedances = [complex(float(r), float(i)) for r, i in zip(reals, imags)]
                # CORRECCIÓN: Se agregan amplitudes y phases vacíos
                return MeasureResult(frequencies=frequencies, amplitudes=[], phases=[], impedances=impedances)
                
            except json.JSONDecodeError:
                # 3. Si falla el JSON, es una lectura de SingleFreq en texto plano
                partes = clean_str.replace("j", "").split()
                if len(partes) >= 2:
                    real_val = float(partes[0])
                    imag_val = float(partes[1])
                    # CORRECCIÓN: Se agregan amplitudes y phases vacíos
                    return MeasureResult(frequencies=[0.0], amplitudes=[], phases=[], impedances=[complex(real_val, imag_val)])
                else:
                    return None

        except Exception as e:
            print(f"Error decodificando en el Adapter: {e}")
            return None