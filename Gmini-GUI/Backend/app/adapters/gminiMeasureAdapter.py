import json
from app.adapters.iMeasureAdapter import IMeasureAdapter
from app.models.measureSetup import MeasureSetup, SingleMeasureSetup, SpecMeasureSetup, MultiMeasureSetup
from app.models.measureResult import MeasureResult

"""
Adaptador concreto para realizar mediciones con la placa Guanaco Mini
Traduce objetos del dominio a comandos de la consola de texto plano
"""
class GminiMeasureAdapter(IMeasureAdapter):
    #Mapea el valor de la resistencia RFB en Ohms al indice que espera la placa, segun la hoja de datos: 0 (470), 1 (150), 2 (1000).
    def _get_rfb_index(self, rfb_value: float) -> int:
        mapeo = {470.0: 0, 150.0: 1, 1000.0: 2}
        return mapeo.get(rfb_value, 0)  #devuelve por defecto 0 si no lo encuentra

    #Genera el bloque de comandos para configurar los componentes analogicos
    def encode_setup(self, setup: MeasureSetup) -> str:
        #Formateamos los comandos segun la especificacion de la consola
        comandos = [
            "outfmt json",
            "impfmt full",
            f"voltage {int(setup._exitation_voltage)}",
            f"gain {int(setup._gain)}",                  
            f"setrfb {self._get_rfb_index(setup._rfbvalue)}",
            f"settcycles {setup._settcycles}",
            f"select {setup._mux_channel[0]}"
        ]
        
        #Unimos todos los comandos con saltos de línea
        return "\n".join(comandos) + "\n"
    #Genera el comando exacto para iniciar la medicion según el tipo de Setup
    def encode_execution(self, setup: MeasureSetup) -> str:
        if isinstance(setup, SingleMeasureSetup):
            return f"singlefreq {setup.freq} {setup.delay} {setup.count}\n"
            
        elif isinstance(setup, SpecMeasureSetup):
            return f"sweep {setup.startfreq} {setup.incfreq} {setup.steps} {setup.repeat}\n"
            
        elif isinstance(setup, MultiMeasureSetup):
            #Se usa delay=0 y count=1 para tomar una muestra rapida por cada frecuencia
            comandos = [f"singlefreq {freq} 0 1" for freq in setup.freq_list]
            return "\n".join(comandos) + "\n"
            
        return "\n"

    def decode(self, response: str) -> MeasureResult:
        frequencies = []
        amplitudes = []
        phases = []
        impedances = []

        try:
            # Procesamiento iterativo: como la multifrecuencia puede devolver múltiples
            # respuestas u objetos JSON encadenados, iteramos sobre cada bloque válido.
            partes = response.split('\n')
            
            for parte in partes:
                parte = parte.strip()
                if not parte:
                    continue
                #Si la placa devolvió JSON
                if parte.startswith('{') and parte.endswith('}'):
                    data = json.loads(parte)
                    result_data = data.get("sweep", {}).get("result", data)

                    #Si es una lista, la extendemos. Si es un valor unico, lo agregamos.
                    if "frequency" in result_data:
                        freq_data = result_data["frequency"]
                        if isinstance(freq_data, list):
                            frequencies.extend(freq_data)
                        else:
                            frequencies.append(freq_data)

                    #Verificamos si es una lista de magnitudes (sweep) o una sola (singlefreq)
                    if "magnitude" in result_data:
                        mag_data = result_data["magnitude"]
                        if isinstance(mag_data[0], list):
                            for mag in mag_data:
                                impedances.append(complex(mag[0], mag[1]))
                        else:
                            impedances.append(complex(mag_data[0], mag_data[1]))
                            
                #Si la placa devolvió texto plano (comportamiento de singlefreq sin JSON)
                elif " " in parte and "j" in parte.lower():
                    # Esto ataja el caso donde singlefreq no formatea en JSON
                    valores = parte.replace('j', '').replace('J', '').split()
                    if len(valores) == 2:
                        impedances.append(complex(float(valores[0]), float(valores[1])))
                        
        except Exception as e:
            print(f"Error al decodificar la respuesta: {e}")

        return MeasureResult(frequencies, amplitudes, phases, impedances)