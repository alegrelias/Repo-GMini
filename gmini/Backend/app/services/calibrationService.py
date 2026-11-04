from app.models.device import Device
from app.models.calibrationSetup import CalibrationSetup
from app.states.deviceState import CalibratedState, UncalibratedState, DeviceErrorState
from app.adapters.iCalibrationAdapter import ICalibrationAdapter
from app.services.connectionService import ConnectionService
from app.services.sessionManager import SessionManager

"""Servicio encargado de orquestar la calibración electrónica del equipo"""
class CalibrationService:
    def __init__(self, 
                 connection_service: ConnectionService, 
                 adapter: ICalibrationAdapter,
                 session_manager: SessionManager):
        self._connection_service = connection_service
        self._adapter = adapter
        self._session_manager = session_manager

    def calibrate_device(self, device: Device, cal_setup: CalibrationSetup) -> bool:
        """Envia la secuencia de configuracion física y calibracion al ESP32. Actualiza el estado del Device segun el resultado"""
        #Verificar usuario activo
        current_user = self._session_manager.get_current_user()
        if not current_user:
            raise PermissionError("Debe haber un usuario activo para calibrar el dispositivo.")
        
        #Verificar Modo experto
        if not self._session_manager.get_active_mode():
            raise PermissionError("La calibración requiere que el Modo Avanzado esté activo.")

        #Traduce el CalibrationSetup a comandos de consola
        command = self._adapter.encode(cal_setup)

        try:
            #Enviar comando y esperar respuesta del hardware
            self._connection_service.send(device, command)
            response = self._connection_service.receive(device)
            
            #Evaluar respuesta mediante el adaptador
            is_success = self._adapter.decode(response)
            
            #Actualizar maquina de estados del dispositivo
            if is_success:
                device.set_state(CalibratedState())
                return True
            else:
                device.set_state(UncalibratedState())
                return False

        except Exception as e:
            device.set_state(DeviceErrorState())
            print(f"Error de comunicación/hardware durante la calibración: {e}")
            return False