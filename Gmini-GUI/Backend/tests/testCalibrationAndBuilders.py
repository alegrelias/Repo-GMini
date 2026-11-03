
import pytest
from unittest.mock import MagicMock


from app.models.device import Device
from app.models.user import User
from app.models.calibrationSetup import CalibrationSetup
from app.models.measureSetup import SingleMeasureSetup, SpecMeasureSetup, MultiMeasureSetup
from app.states.deviceState import CalibratedState, UncalibratedState, DeviceErrorState
from app.builders.singleFreqSetupBuilder import SingleFreqSetupBuilder
from app.builders.spectroSetupBuilder import SpectroSetupBuilder
from app.builders.multiFreqSetupBuilder import MultiFreqSetupBuilder
from app.adapters.gminiCalibrationAdapter import GminiCalibrationAdapter
from app.services.calibrationService import CalibrationService
from app.services.sessionManager import SessionManager




# =====================================================================
# 1. TESTS DE BUILDERS (Patrón Builder)
# =====================================================================
def test_single_freq_setup_builder():
    setup = (
        SingleFreqSetupBuilder()
        .with_freq(50000.0)
        .with_observations("Monofrecuencia 50kHz")
        .build()
    )
    assert isinstance(setup, SingleMeasureSetup)
    assert setup.get_freq() == 50000.0
    assert setup.get_observations() == "Monofrecuencia 50kHz"




def test_spectro_setup_builder():
    setup = (
        SpectroSetupBuilder()
        .with_start_freq(10000.0)
        .with_inc_freq(5000.0)
        .with_steps(10)
        .with_repeat(2)
        .with_observations("Barrido de prueba")
        .build()
    )
    assert isinstance(setup, SpecMeasureSetup)
    assert setup.get_start_freq() == 10000.0
    assert setup.get_inc_freq() == 5000.0
    assert setup.get_steps() == 10
    assert setup.get_repeat() == 2
    assert setup.get_observations() == "Barrido de prueba"




def test_multi_freq_setup_builder():
    freqs = [1000.0, 5000.0, 10000.0, 50000.0]
    setup = (
        MultiFreqSetupBuilder()
        .with_freq_list(freqs)
        .with_observations("Multifrecuencia")
        .build()
    )
    assert isinstance(setup, MultiMeasureSetup)
    assert setup.get_freq_list() == freqs




# =====================================================================
# 2. TESTS DEL ADAPTADOR DE CALIBRACIÓN (GminiCalibrationAdapter)
# =====================================================================
def test_calibration_adapter_encode_and_decode():
    adapter = GminiCalibrationAdapter()
    cal_setup = CalibrationSetup(
        exitation_voltage=400.0, gain=1, rfbvalue=470, settcycles=15, mux_channel=0
    )


    cmd = adapter.encode(cal_setup)
    assert isinstance(cmd, str)
    assert len(cmd) > 0


    # Según Datasheet Rev3 (Pág. 7): sin error no devuelve nada o devuelve confirmación positiva
    assert adapter.decode("0") is True or adapter.decode("") is True


    # Códigos de error documentados en el Datasheet Rev3 (Pág. 7): -1 a -5
    for error_code in ["-1", "-2", "-3", "-4", "-5"]:
        assert adapter.decode(error_code) is False




# =====================================================================
# 3. TESTS DE CALIBRATION SERVICE (Orquestación y Patrón State)
# =====================================================================
def test_calibrate_device_success_transitions_to_calibrated_state():
    device = Device(device_id=1)
    cal_setup = CalibrationSetup(400.0, 1, 470, 15, 0)


    mock_conn = MagicMock()
    mock_conn.receive.return_value = "0"


    mock_adapter = MagicMock()
    mock_adapter.encode.return_value = "calibrate 0\n"
    mock_adapter.decode.return_value = True


    session = SessionManager()
    session.set_current_user(MagicMock(spec=User))
    session.set_active_mode(True)


    service = CalibrationService(mock_conn, mock_adapter, session)
    result = service.calibrate_device(device, cal_setup)


    assert result is True
    assert isinstance(device.get_state(), CalibratedState)
    assert device.can_measure() is True
    mock_conn.send.assert_called_once_with(device, "calibrate 0\n")




def test_calibrate_device_blocked_in_basic_mode():
    device = Device(device_id=1)
    cal_setup = CalibrationSetup(400.0, 1, 470, 15, 0)


    session = SessionManager()
    session.set_current_user(MagicMock(spec=User))
    session.set_active_mode(False)


    service = CalibrationService(MagicMock(), MagicMock(), session)


    with pytest.raises(PermissionError):
        service.calibrate_device(device, cal_setup)




def test_calibrate_device_hardware_error_transitions_to_uncalibrated():
    device = Device(device_id=1)
    cal_setup = CalibrationSetup(400.0, 1, 470, 15, 0)


    mock_conn = MagicMock()
    mock_conn.receive.return_value = "-5"


    mock_adapter = MagicMock()
    mock_adapter.encode.return_value = "calibrate 0\n"
    mock_adapter.decode.return_value = False


    session = SessionManager()
    session.set_current_user(MagicMock(spec=User))
    session.set_active_mode(True)


    service = CalibrationService(mock_conn, mock_adapter, session)
    result = service.calibrate_device(device, cal_setup)


    assert result is False
    assert isinstance(device.get_state(), UncalibratedState)
    assert device.can_measure() is False
