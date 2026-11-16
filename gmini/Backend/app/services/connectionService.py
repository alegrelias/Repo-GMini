from typing import Dict, List, Any
from gmini.Backend.app.core.observer import IObservable, IObserver
from gmini.Backend.app.models.device import Device
from gmini.Backend.app.states.deviceState import DeviceErrorState

import time

"""Servicio encargado de gestionar los enlaces fisicos (puerto serial / bluetooth) con los dispositivos Guanaco Mini"""
class ConnectionService(IObservable, IObserver):
    def __init__(self):
        self.active_connections: Dict[int, Any] = {}
        self._observers: List[IObserver] = []

    def connect(self, device: Device, connection_type: Any) -> bool:
        try:
            connection_type.connect()
            if isinstance(connection_type, IObservable):
                connection_type.attach(self)
            self.active_connections[device.device_id] = connection_type
            self.notify("Conectado")
            return True
        except Exception as e:
            device.set_state(DeviceErrorState())
            self.notify(f"CONNECTION_ERROR: {e}")
            return False

    def send_console_command(self, device: Device, command: str) -> str:
        """
        Envía un comando crudo a la placa, espera la respuesta acumulativa 
        y limpia el prompt. Exclusivo para la consola de diagnóstico.
        """
        conn = self.active_connections.get(device.device_id)
        if not conn:
            raise ConnectionError("El dispositivo no tiene una conexión activa.")
        
        # 1. El hardware exige un salto de linea \n al final del comando
        clean_command = command.strip()
        if not clean_command.endswith('\n'):
            clean_command += '\n'
            
        try:
            conn.send(clean_command)
            
            response_str = ""
            import time
            timeout = time.time() + 3.0  # Timeout de seguridad de 3 segundos
            
            # 2. Acumulala respuesta usando  receive()
            while time.time() < timeout:
                chunk = conn.receive()
                if chunk:
                    # Dependiendo de tu adapter, chunk puede ser bytes o str
                    if isinstance(chunk, bytes):
                        chunk = chunk.decode('utf-8', errors='ignore')
                    response_str += chunk
                
                # El hardware devuelve ad5933> cuando el comando finaliza
                if "ad5933>" in response_str:
                    break
                time.sleep(0.05)
            
            # 3. Limpieza para la UI
            cleaned_response = response_str.replace("ad5933>", "").strip()
            return cleaned_response
            
        except Exception as e:
            raise RuntimeError(f"Fallo en la comunicación serial: {str(e)}")
        
    def disconnect(self, device: Device) -> None:
        conn = self.active_connections.pop(device.device_id, None)
        if conn:
            conn.disconnect()
            self.notify("Desconectado")

    def send(self, device: Device, command: str) -> None:
        conn = self.active_connections.get(device.device_id)
        if not conn:
            raise ConnectionError("El dispositivo no tiene una conexión activa.")
        conn.send(command)

    def receive(self, device: Device) -> str:
        conn = self.active_connections.get(device.device_id)
        if not conn:
            raise ConnectionError("El dispositivo no tiene una conexión activa.")
        return conn.receive()

    def update(self, observable: IObservable, event_info: str) -> None:
        self.notify(event_info)

    def attach(self, observer: IObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: IObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event_info: str = "") -> None:
        for observer in self._observers:
            observer.update(self, event_info)