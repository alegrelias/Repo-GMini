import json
import pytest
from unittest.mock import MagicMock


from app.models.device import Device
from app.models.user import User
from app.models.measure import Measure
from app.models.measureResult import MeasureResult
from app.states.deviceState import CalibratedState, UncalibratedState, DeviceErrorState
from app.builders.singleFreqSetupBuilder import SingleFreqSetupBuilder
from app.builders.spectroSetupBuilder import SpectroSetupBuilder
from app.adapters.gminiMeasureAdapter import GminiMeasureAdapter
from app.services.measureService import MeasureService
from app.services.statisticsService import StatisticsService
from app.services.sessionManager import SessionManager




# =====================================================================
# 1. TESTS DEL ADAPTADOR DE MEDICIÓN (GminiMeasureAdapter)
# =====================================================================
def test_measure_adapter_encode_single_and_sweep():
    adapter = GminiMeasureAdapter()


    single_setup = SingleFreqSetupBuilder().with_freq(1000.0).build()
    cmd_single = adapter.encode_execution(single_setup)
    assert "singlefreq 1000.0" in cmd_single


    sweep_setup = (
        SpectroSetupBuilder()
        .with_start_freq(10000.0)
        .with_inc_freq(20000.0)
        .with_steps(5)
        .with_repeat(1)
        .build()
    )
    cmd_sweep = adapter.encode_execution(sweep_setup)
    assert cmd_sweep == "sweep 10000.0 20000.0 5 1\n"




def test_measure_adapter_decode_datasheet_json():
    adapter = GminiMeasureAdapter()
    # Formato JSON de la hoja de datos Guanaco Mini V2.0 Rev3 (Pág. 13)
    raw_json = json.dumps({
        "impedance": [[38713, -39507], [84984, -42604]],
        "frequency": [10000, 30000]
    })


    result = adapter.decode(raw_json)
    assert isinstance(result, MeasureResult)
    assert result.get_frequencies() == [10000.0, 30000.0]
    assert result.get_impedances() == [complex(38713, -39507), complex(84984, -42604)]




# =====================================================================
# 2. TESTS DE MEASURE SERVICE Y STATISTICS SERVICE
# =====================================================================
def test_execute_measure_blocked_when_uncalibrated():
    device = Device(device_id=1)  # Inicia en UncalibratedState por defecto
    setup = SingleFreqSetupBuilder().with_freq(1000.0).build()
    measure = Measure(measure_setup=setup, device_id=1)


    session = SessionManager()
    session.set_current_user(MagicMock(spec=User))


    service = MeasureService(MagicMock(), MagicMock(), session)


    # CAL-03: No debe permitir medir si el dispositivo está en UncalibratedState
    with pytest.raises(RuntimeError):
        service.execute_measure(device, measure)




def test_execute_measure_success_and_statistics():
    device = Device(device_id=1)
    device.set_state(CalibratedState())


    setup = SingleFreqSetupBuilder().with_freq(10000.0).build()
    measure = Measure(measure_setup=setup, device_id=1)


    mock_conn = MagicMock()
    mock_conn.receive.return_value = '{"impedance": [[500.0, -100.0], [400.0, -50.0]], "frequency": [10000, 20000]}'


    adapter = GminiMeasureAdapter()
    session = SessionManager()
    mock_user = MagicMock(spec=User)
    mock_user.get_id.return_value = 1
    session.set_current_user(mock_user)


    service = MeasureService(mock_conn, adapter, session)
    success = service.execute_measure(device, measure)


    assert success is True
    assert measure.get_state() == 'COMPLETE'
    assert isinstance(device.get_state(), CalibratedState)


    # Validar StatisticsService sobre medición COMPLETE (MED-11)
    stats = StatisticsService.calculate_basic_stats(measure)
    assert "error" not in stats
    assert stats["imp_real_mean"] == 450.0
    assert stats["imp_imag_mean"] == -75.0




def test_execute_measure_io_error_triggers_emergency_save():
    device = Device(device_id=1)
    device.set_state(CalibratedState())


    setup = SingleFreqSetupBuilder().with_freq(10000.0).build()
    measure = Measure(measure_setup=setup, device_id=1)


    mock_conn = MagicMock()
    mock_conn.send.side_effect = ConnectionError("Pérdida repentina de señal USB")


    mock_db = MagicMock()
    session = SessionManager()
    mock_user = MagicMock(spec=User)
    mock_user.get_id.return_value = 1
    session.set_current_user(mock_user)


    service = MeasureService(mock_conn, GminiMeasureAdapter(), session, db_service=mock_db)
    success = service.execute_measure(device, measure)


    assert success is False
    assert measure.get_state() == 'ERROR'
    assert isinstance(device.get_state(), DeviceErrorState)
    # MED-14: Debe invocar save_measure en DataBaseService ante caída de señal
    mock_db.save_measure.assert_called_once_with(1, measure)
