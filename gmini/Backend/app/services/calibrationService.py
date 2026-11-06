from gmini.Backend.app.models.device import Device
from gmini.Backend.app.models.calibrationSetup import CalibrationSetup
from gmini.Backend.app.states.deviceState import CalibratedState, UncalibratedState, DeviceErrorState
from gmini.Backend.app.adapters.iCalibrationAdapter import ICalibrationAdapter
from gmini.Backend.app.services.connectionService import ConnectionService
from gmini.Backend.app.services.sessionManager import SessionManager

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
        #Verificar únicamente que exista un usuario con sesión iniciada
        current_user = self._session_manager.get_current_user()
        if not current_user:
            raise PermissionError("Debe haber un usuario activo para calibrar el dispositivo.")

        #Codificar el CalibrationSetup a comandos de la placa
        command = self._adapter.encode(cal_setup)

        try:
            #Enviar comando y recibir respuesta
            self._connection_service.send(device, command)
            response = self._connection_service.receive(device)

            #Decodificar respuesta y actualizar estado del dispositivo
            is_success = self._adapter.decode(response)

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